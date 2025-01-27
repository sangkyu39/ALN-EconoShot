from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def analyze(data: dict):
    text = data.get("text", "")
    result = ""
    return result