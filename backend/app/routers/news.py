from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_news():
    news = ""
    return {"news": news}