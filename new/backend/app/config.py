import os
from dotenv import load_dotenv

load_dotenv()

BING_API_KEY = os.getenv("BING_API_KEY")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
DART_API_KEY = os.getenv("DART_API_KEY")

# 예: DART에서 가져올 때 시총 기준 (자본금, 자산 등으로 임의 필터링 가능)
MARKET_CAP_THRESHOLD = 10_000_000_000  # 예: 100억
