import json
import re
from .config import ROOT


def run_directory(label):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,48}', label):
        raise ValueError('Label run hanya boleh huruf, angka, underscore, atau tanda minus (1–48 karakter).')
    return ROOT / 'output' / label


def create_run(label):
    target = run_directory(label)
    if target.exists():
        raise ValueError(f'Run {label!r} sudah ada. Gunakan label baru agar baseline tidak tertimpa.')
    target.mkdir(parents=True)
    return target


def append_jsonl(target, value):
    with target.open('a', encoding='utf-8') as f:
        f.write(json.dumps(value, ensure_ascii=False) + '\n')


def save_request(folder, result, trace, events):
    append_jsonl(folder/'results.jsonl', result)
    append_jsonl(folder/'traces.jsonl', trace)
    for event in events:
        append_jsonl(folder/'events.jsonl', event)


def read_jsonl(target):
    return [json.loads(line) for line in target.read_text(encoding='utf-8').splitlines() if line.strip()]
