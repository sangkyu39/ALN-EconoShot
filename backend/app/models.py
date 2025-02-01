from pydantic import BaseModel
from typing import List, Optional

# 기존에 분석한 뉴스 조회용 모델
class NewsItem(BaseModel):
    title: str
    link: str
    summary: str
    sentiment: str
    companies: List[str]
    industries: List[str]

# 기업 정보 모델
class CompanyItem(BaseModel):
    corp_name: str
    stock_code: str
    country: str     # "KR" or "US" 등
    industry: str
    market_cap: int  # 시가총액
