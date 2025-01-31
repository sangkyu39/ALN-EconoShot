from fastapi import FastAPI
from .database import create_tables
from .routers import news_router, companies_router

def create_app() -> FastAPI:
    app = FastAPI()

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
