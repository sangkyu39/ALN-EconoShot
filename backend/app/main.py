# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import news  # news.py의 router를 가져옴


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React 개발 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(news.router, prefix="/news", tags=["news"])  # router로 등록
@app.get("/")
def read_root():
    return {"message": "Welcome to the Sentiment Analysis API"}
