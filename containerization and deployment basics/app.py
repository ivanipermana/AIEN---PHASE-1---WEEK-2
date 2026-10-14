import logging
import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentiment import MODEL, predict

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
logger = logging.getLogger('sentiment_api')
app = FastAPI(title='Sentiment API — Docker Lab', version='1.0.0',
              description='Model Naive Bayes demonstrasi, bukan model produksi.')

class PredictionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000)

@app.get('/health')
def health():
    return {'status': 'ok', 'app_name': os.getenv('APP_NAME', 'Sentiment Lab'),
            'model_version': MODEL['version']}

@app.post('/predict')
def prediction(request: PredictionRequest):
    result = predict(request.text)
    logger.info('prediction sentiment=%s known_tokens=%s', result['sentiment'], result['known_tokens'])
    return result
