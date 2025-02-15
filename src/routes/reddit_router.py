from dotenv import load_dotenv
from models import LLMOptions
from utils_general import get_logger
from utils_llm import summarize_news
from fastapi import APIRouter, HTTPException
from reddit_extractor import search_posts_by_text, get_hot_news


load_dotenv()
router = APIRouter()
logger = get_logger()


def summarize_posts(posts):
    """
    Realiza a sumarização dos posts, calculando contagens de sentimentos, agregando palavras-chave e somando os scores dos posts.

    Parâmetros:
        posts (list[dict]): Lista de dicionários representando os posts. Cada dicionário deve conter as chaves:
            - "sentiment": string que pode ser "Positivo", "Negativo" ou "Neutro".
            - "keywords": valor representativo das palavras-chave associadas ao post.
            - "score": valor numérico (ou string numérica) que representa o score do post.

    Retorna:
        dict: Um dicionário contendo os seguintes itens:
            - "positive" (int): Número de posts com sentimento "Positivo".
            - "negative" (int): Número de posts com sentimento "Negativo".
            - "neutro" (int): Número de posts com sentimento "Neutro".
            - "keywords" (list): Lista com os valores das chaves "keywords" de cada post.
            - "score_total" (int): Soma total dos scores dos posts, após conversão para inteiro.
    """
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


@router.post("/get_sentiment/v1")
def analyze_sentiment(text: str, n_posts: int):
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
    logger.info(f"Posts recebidos com sucesso.")

    return summarize_posts(posts)


@router.post("/get_hot_news/v1")
def analyze_news(n_posts: int):
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
    logger.info(f"Posts recebidos com sucesso.")
    return summarize_news(news)


@router.post("/get_sentiment/v2")
def analyze_sentiment(text: str, n_posts: int, llm_option: LLMOptions):
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
    logger.info(f"Posts recebidos com sucesso.")

    return summarize_posts(posts)


# @router.post("/get_hot_news/v2")
# def analyze_news(n_posts: int, llm_option=LLMOptions):
#     """
#     Analisa um número de posts de notícias.

#     Parâmetros:
#         n_posts (int): Número de posts a serem analisados. Se for maior que 100, a função levanta uma exceção.

#     Exceções:
#         HTTPException: Levantada quando n_posts é maior que 100, indicando que o número de posts solicitado está muito grande.

#     Retorna:
#         Resumo das notícias obtidas a partir dos posts quentes.
#     """
#     if n_posts > 100:
#         raise HTTPException(
#             status_code=400,
#             detail="O tamanho do número de posts está muito grande.",
#         )
#     news = get_hot_news(n_posts)
#     logger.info(f"Posts recebidos com sucesso.")
#     return summarize_news(news, llm_option)
