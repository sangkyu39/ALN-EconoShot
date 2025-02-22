from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup
from typing import List
import logging

from ..config import BING_API_KEY, NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from ..database import get_db
from ..models import NewsItem
from ..ml.sentiment_analyzer import analyze_sentiment
from ..ml.industry_extractor import extract_industries

router = APIRouter()
logger = logging.getLogger(__name__)

# -------------------------
# [1] 뉴스 가져와서 분석 후 DB 저장 (새로고침 시)
# -------------------------

def fetch_news_from_bing(query: str):
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
    params = {"q": query, "mkt": "en-US", "count": 2}
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for item in data.get("value", []):
            articles.append({
                "title": item.get("name", ""),
                "link": item.get("url", ""),
                "description": item.get("description", "")
            })
        return articles
    except Exception as e:
        logger.error(f"Failed to fetch Bing news: {e}")
        return []

def fetch_news_from_naver(query: str):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {
        "query": f"{query} 산업 주가 증권",
        "display": 4,
        "start": 1,
        "sort": "sim"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []
        for item in data.get("items", []):
            articles.append({
                "title": BeautifulSoup(item.get("title"), "html.parser").get_text(),
                "link": item.get("link", ""),
                "description": BeautifulSoup(item.get("description"), "html.parser").get_text()
            })
        return articles
    except Exception as e:
        logger.error(f"Failed to fetch Naver news: {e}")
        return []

def load_company_names():
    """
    DB에서 모든 기업명(국내+해외) 로드해 set으로 반환.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT corp_name FROM companies")
    rows = cur.fetchall()
    conn.close()
    return {row["corp_name"] for row in rows}

def extract_companies_from_text(text: str, company_list: set):
    found = []
    lower_text = text.lower()
    for comp in company_list:
        if comp.lower() in lower_text:
            found.append(comp)
    return list(set(found))

@router.get("/fetch-latest", response_model=List[NewsItem])
def fetch_latest_news(query: str = "경제"):
    """
    [API 1] 최신 기사를 새로 가져와서 분석 & DB 저장
    """
    # (1) 뉴스 가져오기
    # bing_articles = fetch_news_from_bing(query)
    naver_articles = fetch_news_from_naver(query)
    all_articles = naver_articles
    print("뉴스 가져옴")
    # (2) DB 연결
    conn = get_db()
    cur = conn.cursor()

    # (3) 기업명 로드
    company_list = load_company_names()
    print("기업 로드")
    # (4) 분석 후 DB 저장
    processed_data = []
    for article in all_articles:
        title = article["title"]
        link = article["link"]
        summary = article["description"]

        # 감성분석
        sentiment = analyze_sentiment(summary)
        print("감정분석")
        # 기업 추출
        found_companies = extract_companies_from_text(summary, company_list)
        print("기업 추출")
        # 산업 추출
        industries = extract_industries(summary)
        print("산업추출")
        processed_data.append({
            "title": title,
            "link": link,
            "summary": summary,
            "sentiment": sentiment,
            "companies": found_companies,
            "industries": industries
        })

        # DB 삽입
        cur.execute("""
            INSERT INTO news (title, link, summary, sentiment, companies, industries)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            title,
            link,
            summary,
            sentiment,
            ",".join(found_companies),
            ",".join(industries)
        ))
    conn.commit()
    conn.close()

    return processed_data

# -------------------------
# [2] DB에 저장된 기사 조회
# -------------------------
@router.get("/get-stored", response_model=List[NewsItem])
def get_stored_news():
    """
    [API 2] 이미 DB에 저장된 기사들을 가져오기
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, link, summary, sentiment, companies, industries
        FROM news
        ORDER BY created_at DESC
        LIMIT 100
    """)
    rows = cur.fetchall()
    conn.close()

    results = []
    for r in rows:
        comps = r["companies"].split(",") if r["companies"] else []
        inds = r["industries"].split(",") if r["industries"] else []
        results.append({
            "title": r["title"],
            "link": r["link"],
            "summary": r["summary"],
            "sentiment": r["sentiment"],
            "companies": comps,
            "industries": inds,
        })
    return results
