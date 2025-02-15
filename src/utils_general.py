import os
import logging
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = int(os.getenv("API_TOKEN", 1234))


def get_logger():
    """
    Cria e configura um logger para a aplicação FastAPI.

    Esta função configura o logger com nível de log INFO e define o formato das mensagens. Em seguida, retorna uma instância do logger identificada como 'fastapi'.

    Returns:
        logging.Logger: Instância configurada do logger.
    """
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
    )
    return logging.getLogger("fastapi")


def common_verificacao_api_token(api_token: int):
    """
    Verifica se o token de API fornecido é válido.

    Parâmetros:
        api_token (int): Token de API fornecido para verificação.

    Exceções:
        HTTPException: Se o token fornecido não corresponder ao token esperado (API_TOKEN),
                       levantando uma exceção com status 401 e detalhe "Token inválido".
    """
    if api_token != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
        )


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
