"""Inferensi model Naive Bayes kecil; hanya memakai Python standard library."""
import json
import math
import re
from pathlib import Path

MODEL = json.loads((Path(__file__).parent / 'data/model.json').read_text(encoding='utf-8'))
VOCABULARY = set(MODEL['vocabulary'])

def predict(text: str) -> dict:
    words = re.findall(r'[a-z]+', text.lower())
    known = [word for word in words if word in VOCABULARY]
    if not known:
        return {'sentiment': 'unknown', 'demo_score': None, 'known_tokens': 0,
                'model_version': MODEL['version']}
    scores = {
        label: MODEL['log_prior'][label] + sum(MODEL['log_likelihood'][label][word] for word in known)
        for label in MODEL['labels']
    }
    best = max(scores, key=scores.get)
    peak = scores[best]
    denominator = sum(math.exp(value - peak) for value in scores.values())
    return {'sentiment': best, 'demo_score': round(1 / denominator, 4),
            'known_tokens': len(known), 'model_version': MODEL['version']}
