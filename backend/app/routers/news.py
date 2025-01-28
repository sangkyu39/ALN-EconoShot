from fastapi import APIRouter
import requests
from transformers import pipeline
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import dart_fss as dart
import json
import time

router = APIRouter()

# .env 파일에서 환경 변수 로드
load_dotenv()

# 상장 기업 데이터 파일 경로
COMPANY_FILE = "korean_companies.json"

# DART API 키 설정
dart_api_key = os.getenv('DART_API_KEY')
dart.set_api_key(dart_api_key)

# 상장 기업 목록 로드 및 저장 함수
def save_korean_companies():
    try:
        corp_list = dart.get_corp_list()
        listed_companies = [
            {"corp_name": corp.info["corp_name"], "stock_code": corp.info["stock_code"]}
            for corp in corp_list
            if corp.info.get("stock_code")
        ]
        with open(COMPANY_FILE, "w", encoding="utf-8") as file:
            json.dump(listed_companies, file, ensure_ascii=False, indent=4)
        print(f"{len(listed_companies)}개의 상장 기업 정보를 저장했습니다.")
    except Exception as e:
        print(f"상장 기업 목록 저장 실패: {e}")

# 저장된 상장 기업 목록 읽기
def load_korean_companies():
    if not os.path.exists(COMPANY_FILE):
        print("상장 기업 데이터 파일이 없습니다. 데이터를 새로 저장합니다.")
        save_korean_companies()
    try:
        with open(COMPANY_FILE, "r", encoding="utf-8") as file:
            companies = json.load(file)
            return {company["corp_name"] for company in companies}
    except Exception as e:
        print(f"상장 기업 목록 로드 실패: {e}")
        return set()

# 뉴스 수집 함수 (Bing News API)
def fetch_news_from_bing(query):
    api_key = os.getenv('BING_API_KEY')
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"

    if not api_key or not endpoint:
        raise ValueError("Bing API Key 또는 Endpoint가 환경 변수에 설정되지 않았습니다.")

    params = {
        'q': f"{query}",
        'mkt': 'en-US',
        'count': 10,
    }
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        news_data = response.json()
        articles = []
        for item in news_data.get('value', []):
            title = item.get('name')
            link = item.get('url')
            description = item.get('description')
            articles.append({'title': title, 'link': link, 'description': description})
        return articles
    except requests.exceptions.HTTPError as err:
        print(f"API 호출 실패: {err}")
        return None

# 뉴스 수집 함수 (네이버 뉴스 API)
def fetch_news_from_naver(query):
    client_id = os.getenv('NAVER_CLIENT_ID')
    client_secret = os.getenv('NAVER_CLIENT_SECRET')

    if not client_id or not client_secret:
        raise ValueError("네이버 클라이언트 ID 또는 시크릿이 환경 변수에 설정되지 않았습니다.")

    params = {
        'query': f"{query} 경제 금융",
        'display': 10,
        'start': 1,
        'sort': 'sim',
    }
    headers = {
        'X-Naver-Client-Id': client_id,
        'X-Naver-Client-Secret': client_secret,
    }

    try:
        response = requests.get('https://openapi.naver.com/v1/search/news.json', headers=headers, params=params)
        response.raise_for_status()
        news_data = response.json()
        articles = []
        for item in news_data.get('items', []):
            title = BeautifulSoup(item.get('title'), 'html.parser').get_text()
            link = item.get('link')
            description = BeautifulSoup(item.get('description'), 'html.parser').get_text()
            articles.append({'title': title, 'link': link, 'description': description})
        return articles
    except requests.exceptions.HTTPError as err:
        print(f"API 호출 실패: {err}")
        return None

# 감성 분석 파이프라인
def analyze_sentiment(text):
    sentiment_analyzer = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    result = sentiment_analyzer(text)
    label = result[0]['label']
    if label in ['1 star', '2 stars']:
        return '부정'
    elif label in ['4 stars', '5 stars']:
        return '긍정'
    else:
        return '중립'

# 기업명 추출 함수
def extract_companies(text, company_list):
    found_companies = []
    text = text.lower()
    for company in company_list:
        if company.lower() in text:
            found_companies.append(company)
    return found_companies

# 뉴스와 감성 분석 결합
def process_news_data(news_data, company_list):
    processed_data = []
    for article in news_data:
        title = article['title']
        link = article['link']
        description = article['description']
        sentiment = analyze_sentiment(description)
        companies = extract_companies(description, company_list)
        processed_data.append({
            "title": title,
            "link": link,
            "summary": description,
            "sentiment": sentiment,
            "companies": companies
        })
    return processed_data

# 뉴스 데이터 가져오기 엔드포인트
@router.get("/")
async def get_news(query: str = "economy"):
    korean_companies = load_korean_companies()

    bing_news_data = fetch_news_from_bing(query)
    naver_news_data = fetch_news_from_naver(query)
    all_news_data = (bing_news_data if bing_news_data else []) + (naver_news_data if naver_news_data else [])

    if all_news_data:
        processed_news = process_news_data(all_news_data, korean_companies)
        return processed_news
    else:
        return {"message": "뉴스 데이터를 가져오는 데 실패했습니다."}