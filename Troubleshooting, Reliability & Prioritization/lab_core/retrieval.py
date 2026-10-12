import json
import re
from .config import ROOT


def retrieve(question, tasks, top_k=2):
    manifest = json.loads((ROOT / 'data/manifest.json').read_text(encoding='utf-8'))
    version = tasks.choose_document_version(manifest)
    if version not in manifest['versions']:
        raise ValueError('Versi dokumen tidak terdaftar dalam manifest.')
    if not isinstance(top_k, int) or top_k < 1:
        raise ValueError('top_k harus bilangan bulat positif.')
    # Path hanya berasal dari manifest paket, bukan input pengguna.
    documents = json.loads((ROOT / manifest['versions'][version]).read_text(encoding='utf-8'))
    words = set(re.findall(r'\w+', question.lower()))
    ranked = []
    for document in documents:
        matches = words.intersection(document['keywords'])
        if matches:
            ranked.append((len(matches), document))
    ranked.sort(key=lambda item: (-item[0], item[1]['id']))
    selected = [document for _, document in ranked[:top_k]]
    return selected, {'index_version': version, 'current_version': manifest['current_version'],
                      'document_ids': [d['id'] for d in selected], 'document_count': len(selected)}
