import json
import math
import statistics
from .config import ROOT, FAQ_URL


def load_cases():
    return json.loads((ROOT/'data/test_cases.json').read_text(encoding='utf-8'))


def grade(case, result):
    answer = result['answer'].lower()
    reasons = []
    if result['status'] != case['expected_status']:
        reasons.append(f"status harus {case['expected_status']}, aktual {result['status']}")
    for word in case.get('required_all', []):
        if word.lower() not in answer:
            reasons.append(f"jawaban tidak memuat {word!r}")
    for word in case.get('forbidden', []):
        if word.lower() in answer:
            reasons.append(f"jawaban masih memuat {word!r}")
    source = case.get('expected_source')
    if source and (source not in result['source_ids'] or f'[{source}]' not in result['answer']):
        reasons.append('ID sumber yang diharapkan tidak ditemukan dalam retrieval/jawaban')
    if case['scenario'] == 'timeout' and FAQ_URL not in result['answer']:
        reasons.append('fallback belum menyertakan FAQ resmi')
    return {'case_id': case['id'], 'category': case['category'], 'passed': not reasons,
            'reasons': reasons, **result}


def metrics(results):
    total = len(results)
    ok = [r for r in results if r['status'] == 'ok']
    degraded = [r for r in results if r['status'] == 'degraded']
    errors = [r for r in results if r['status'] == 'error']
    values = sorted(r['duration_ms'] for r in ok)
    return {'case_count': total, 'quality_pass_count': sum(r['passed'] for r in results),
            'quality_pass_rate': sum(r['passed'] for r in results)/total if total else None,
            'ok_count': len(ok), 'degraded_count': len(degraded), 'error_count': len(errors),
            'ok_rate': len(ok)/total if total else None,
            'served_rate': (len(ok)+len(degraded))/total if total else None,
            'error_rate': len(errors)/total if total else None,
            'p95_ok_ms': values[math.ceil(.95*len(values))-1] if values else None,
            'mean_ok_ms': statistics.mean(values) if values else None,
            'definition': 'ok = jalur model sukses; degraded = fallback; served = ok + degraded. '
                          'p95 nearest-rank pada status ok saja. Quality dari checker lokal sederhana.'}
