from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli")

INDUSTRY_CANDIDATES = [
    "IT", "금융", "제조", "자동차", "바이오", "통신", "서비스", "반도체", "화학"
]

def extract_industries(text: str) -> list:
    result = classifier(
        text[:512],
        candidate_labels=INDUSTRY_CANDIDATES,
        multi_label=True
    )
    industries = []
    for label, score in zip(result["labels"], result["scores"]):
        if score > 0.2:
            industries.append(label)
    return industries
