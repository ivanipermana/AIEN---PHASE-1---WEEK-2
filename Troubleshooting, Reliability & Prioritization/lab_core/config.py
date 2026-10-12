from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FAQ_URL = 'https://support.example.com/faq'  # Alamat fiktif untuk latihan.
MAX_RETRIES = 1  # 1 retry berarti maksimum 2 percobaan, bukan 1 percobaan.
MOCK_TIMEOUT_S = 0.05
LIVE_TIMEOUT_S = 20.0
BACKOFF_BASE_S = 0.005
TOP_K = 2
