from transformers import pipeline

sentiment_pipeline = pipeline(
    'sentiment-analysis',
    model='nlptown/bert-base-multilingual-uncased-sentiment'
)

def analyze_sentiment(text: str) -> str:
    # 너무 긴 경우 앞 부분만 잘라서 처리
    result = sentiment_pipeline(text[:512])[0]
    label = result["label"]
    if label in ['1 star', '2 stars']:
        return "부정"
    elif label in ['4 stars', '5 stars']:
        return "긍정"
    else:
        return "중립"
