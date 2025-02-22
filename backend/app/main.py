from fastapi import FastAPI
from .database import create_tables
from .routers import news_router, companies_router

from fastapi.middleware.cors import CORSMiddleware




def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용 (보안상 필요한 경우 특정 도메인으로 제한 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

    @app.on_event("startup")
    def on_startup():
        create_tables()

    app.include_router(companies_router.router, prefix="/companies", tags=["companies"])
    app.include_router(news_router.router, prefix="/news", tags=["news"])

    @app.get("/")
    def root():
        return {"message": "Hello World"}

    return app

app = create_app()
