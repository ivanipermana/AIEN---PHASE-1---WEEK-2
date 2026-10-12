import time
import uuid
import random
from datetime import datetime, timezone
from . import config
from .model import ModelAdapter, ModelTimeout
from .retrieval import retrieve


class FAQApplication:
    def __init__(self, tasks, provider='mock'):
        self.tasks = tasks
        self.adapter = ModelAdapter(provider)
        self.provider = provider

    def ask(self, question, scenario='normal', request_id=None, top_k=None):
        if not question.strip():
            raise ValueError('Pertanyaan tidak boleh kosong.')
        if scenario not in ('normal', 'timeout', 'transient_timeout'):
            raise ValueError('Skenario tidak dikenal.')
        start = time.perf_counter()
        trace = {'request_id': request_id or uuid.uuid4().hex[:12],
                 'timestamp': datetime.now(timezone.utc).isoformat(),
                 'provider': self.provider, 'scenario': scenario,
                 'duration_ms': None, 'status': 'unknown', 'spans': []}
        events = []
        result = {'request_id': trace['request_id'], 'question': question,
                  'status': 'error', 'answer': '', 'error_type': None, 'source_ids': []}
        try:
            step = time.perf_counter()
            documents, metadata = retrieve(question, self.tasks,
                                            config.TOP_K if top_k is None else top_k)
            trace['spans'].append({'name': 'retrieval', 'status': 'ok',
                   'duration_ms': round((time.perf_counter()-step)*1000, 3), **metadata})
            result['source_ids'] = metadata['document_ids']
            timeout_s = config.MOCK_TIMEOUT_S if self.provider == 'mock' else config.LIVE_TIMEOUT_S
            answer = None
            usage = {}
            for attempt in range(1, config.MAX_RETRIES + 2):
                step = time.perf_counter()
                try:
                    answer, usage = self.adapter.generate(question, documents, scenario, attempt, timeout_s)
                    trace['spans'].append({'name': 'generation', 'attempt': attempt,
                           'status': 'ok', 'duration_ms': round((time.perf_counter()-step)*1000, 3), **usage})
                    result['status'] = 'ok'
                    break
                except ModelTimeout as error:
                    trace['spans'].append({'name': 'generation', 'attempt': attempt,
                           'status': 'error', 'duration_ms': round((time.perf_counter()-step)*1000, 3),
                           'error_type': 'ModelTimeout'})
                    events.append({'request_id': trace['request_id'], 'event': 'model_timeout',
                                   'attempt': attempt, 'max_attempts': config.MAX_RETRIES+1})
                    if attempt <= config.MAX_RETRIES:
                        # Bounded exponential backoff + jitter. Timeout retry untuk panggilan teks,
                        # tidak boleh disalin begitu saja untuk tool dengan efek samping.
                        delay = config.BACKOFF_BASE_S * 2**(attempt-1) + random.uniform(0, 0.003)
                        events.append({'request_id': trace['request_id'], 'event': 'retry_scheduled',
                                       'delay_ms': round(delay*1000, 3)})
                        time.sleep(delay)
                        continue
                    step = time.perf_counter()
                    answer = self.tasks.fallback_for_timeout(error, config.FAQ_URL)
                    if not isinstance(answer, str) or not answer.strip():
                        raise ValueError('Fallback harus berupa pesan non-kosong.')
                    trace['spans'].append({'name': 'fallback', 'status': 'ok',
                           'duration_ms': round((time.perf_counter()-step)*1000, 3)})
                    result['status'] = 'degraded'
                    events.append({'request_id': trace['request_id'], 'event': 'fallback_used'})
            result['answer'] = answer or ''
        except Exception as error:
            result['status'] = 'error'
            result['error_type'] = type(error).__name__
            events.append({'request_id': trace['request_id'], 'event': 'request_failed',
                           'error_type': type(error).__name__})
        finally:
            result['duration_ms'] = round((time.perf_counter()-start)*1000, 3)
            completed = self.tasks.complete_trace(trace, result['duration_ms'], result['status'])
            if not isinstance(completed, dict):
                raise ValueError('complete_trace() harus mengembalikan dict.')
            trace = completed
        return result, trace, events
