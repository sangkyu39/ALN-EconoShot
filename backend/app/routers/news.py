from fastapi import APIRouter
import requests
from transformers import pipeline
import spacy
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

router = APIRouter()

# .env 파일에서 환경 변수 로드
load_dotenv()

# 뉴스 수집 함수 (Bing News API)
def fetch_news_from_bing(query):
    api_key = os.getenv('BING_API_KEY')
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
    
    if not api_key or not endpoint:
        raise ValueError("Bing API Key 또는 Endpoint가 환경 변수에 설정되지 않았습니다.")
    
    params = {
        'q': f"{query} 경제 금융",  # 검색할 키워드에 '경제 금융' 추가
        'mkt': 'ko-KR',
        'count': 5,
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
        'query': f"{query} 경제 금융",  # 검색할 키워드에 '경제 금융' 추가
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
            title = BeautifulSoup(item.get('title'), 'html.parser').get_text()  # HTML 태그 제거
            link = item.get('link')
            description = BeautifulSoup(item.get('description'), 'html.parser').get_text()  # HTML 태그 제거
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
    # 레이블을 '긍정', '부정' 등으로 변환
    if label in ['1 star', '2 stars']:
        return '부정'
    elif label in ['4 stars', '5 stars']:
        return '긍정'
    else:
        return '중립'

# 기업명 추출 함수
def extract_companies(text, nlp_model):
    doc = nlp_model(text)
    companies = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
    return companies

# 뉴스와 감성 분석 결합
def process_news_data(news_data, nlp_model):
    processed_data = []
    for article in news_data:
        title = article['title']
        link = article['link']
        description = article['description']
        sentiment = analyze_sentiment(description)
        companies = extract_companies(description, nlp_model)
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
async def get_news(query: str = "경제"):
    nlp_model = spacy.load('en_core_web_sm')  # 기업명 추출을 위한 SpaCy 모델 로딩
    
    # Bing API에서 뉴스 데이터 가져오기
    bing_news_data = fetch_news_from_bing(query)
    # 네이버에서 뉴스 데이터 가져오기
    naver_news_data = fetch_news_from_naver(query)
    # 두 가지 소스에서 뉴스 데이터 결합
    all_news_data = (bing_news_data if bing_news_data else []) + (naver_news_data if naver_news_data else [])

    if all_news_data:
        processed_news = process_news_data(all_news_data, nlp_model)
        return processed_news
    else:
        return {"message": "뉴스 데이터를 가져오는 데 실패했습니다."}
