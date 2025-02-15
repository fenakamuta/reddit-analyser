from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from reddit_extractor import search_posts_by_text, get_hot_news
from utils_llm import summarize_news


load_dotenv()
router = APIRouter()


def summarize_posts(posts):
    positive = len([post for post in posts if post["sentiment"] == "Positivo"])
    negative = len([post for post in posts if post["sentiment"] == "Negativo"])
    neutro = len([post for post in posts if post["sentiment"] == "Neutro"])
    keywords = [post["keywords"] for post in posts]
    score_total = sum([int(post["score"]) for post in posts])

    return {
        "positive": positive,
        "negative": negative,
        "neutro": neutro,
        "keywords": keywords,
        "score_total": score_total,
    }


@router.post("/get_sentiment")
def analyze_sentiment(text: str, n_posts: int):
    if n_posts > 20:
        raise HTTPException(
            status_code=400,
            detail="O tamanho do número de posts está muito grande.",
        )
    posts = search_posts_by_text(text, n_posts)
    return summarize_posts(posts)


@router.post("/get_hot_news")
def analyze_news(n_posts: int):
    if n_posts > 100:
        raise HTTPException(
            status_code=400,
            detail="O tamanho do número de posts está muito grande.",
        )
    news = get_hot_news(n_posts)
    return summarize_news(news)


if __name__ == "__main__":
    text = input("type the text: ")
    print(get_posts(text))
