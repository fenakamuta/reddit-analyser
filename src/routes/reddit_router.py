from dotenv import load_dotenv
from models import LLMOptions
from utils_general import get_logger, summarize_posts
from utils_llm import summarize_news
from fastapi import APIRouter, HTTPException
from reddit_extractor import search_posts_by_text, get_hot_news


load_dotenv()
router = APIRouter()
logger = get_logger()


@router.post("/get_sentiment/v1")
def analyze_sentiment_v1(text: str, n_posts: int):
    """
    Analisa o sentimento de posts do Reddit com base em um texto de busca.

    Parâmetros:
        text (str): Critério de busca.
        n_posts (int): Número de posts (máx. 20).

    Retorna:
        Resumo gerado por 'summarize_posts'.

    Exceções:
        HTTPException: Se n_posts > 20.
    """
    if n_posts > 20:
        logger.error(f"Erro ao buscar posts sobre {text}.")
        raise HTTPException(
            status_code=400,
            detail="O tamanho do número de posts está muito grande.",
        )
    posts = search_posts_by_text(text, n_posts)
    logger.info("Posts recebidos com sucesso.")

    return summarize_posts(posts)


@router.post("/get_hot_news/v1")
def analyze_news_v1(n_posts: int):
    """
    Analisa um número de posts de notícias.

    Parâmetros:
        n_posts (int): Número de posts a serem analisados. Se for maior que 100, a função levanta uma exceção.

    Exceções:
        HTTPException: Levantada quando n_posts é maior que 100, indicando que o número de posts solicitado está muito grande.

    Retorna:
        Resumo das notícias obtidas a partir dos posts quentes.
    """
    if n_posts > 100:
        raise HTTPException(
            status_code=400,
            detail="O tamanho do número de posts está muito grande.",
        )
    news = get_hot_news(n_posts)
    logger.info("Posts recebidos com sucesso.")
    return summarize_news(news)


@router.post("/get_sentiment/v2")
def analyze_sentiment_v2(text: str, n_posts: int, llm_option: LLMOptions):
    """
    Analisa o sentimento de posts do Reddit com base em um texto de busca.

    Parâmetros:
        text (str): Critério de busca.
        n_posts (int): Número de posts (máx. 20).
        ll_options (LLMOptions): LLMs disponíveis (default o1-mini).

    Retorna:
        Resumo gerado por 'summarize_posts'.

    Exceções:
        HTTPException: Se n_posts > 20.
    """
    if n_posts > 20:
        logger.error(f"Erro ao buscar posts sobre {text}.")
        raise HTTPException(
            status_code=400,
            detail="O tamanho do número de posts está muito grande.",
        )
    posts = search_posts_by_text(text, n_posts, llm_option)
    logger.info("Posts recebidos com sucesso.")

    return summarize_posts(posts)


@router.post("/get_hot_news/v2")
def analyze_news_v2(n_posts: int, llm_option=LLMOptions):
    """
    Analisa um número de posts de notícias.

    Parâmetros:
        n_posts (int): Número de posts a serem analisados. Se for maior que 100, a função levanta uma exceção.

    Exceções:
        HTTPException: Levantada quando n_posts é maior que 100, indicando que o número de posts solicitado está muito grande.

    Retorna:
        Resumo das notícias obtidas a partir dos posts quentes.
    """
    if n_posts > 100:
        raise HTTPException(
            status_code=400,
            detail="O tamanho do número de posts está muito grande.",
        )
    news = get_hot_news(n_posts)
    logger.info("Posts recebidos com sucesso.")
    return summarize_news(news, llm_option)
