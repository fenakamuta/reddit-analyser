import os
import praw
from utils_llm import classify_sentiment, get_keyword


def get_reddit_client():
    """
    Retorna uma instância do cliente do Reddit.

    Retorna:
        praw.Reddit: Instância do cliente do Reddit.
    """
    reddit = praw.Reddit(
        client_id=os.environ.get("REDDIT_CLIENT_KEY"),
        client_secret=os.environ.get("REDDIT_SECRET_KEY"),
        password=os.environ.get("REDDIT_PASSWORD"),
        user_agent=os.environ.get("REDDIT_USER_AGENT"),
        username=os.environ.get("REDDIT_USERNAME"),
    )
    reddit.read_only = True
    return reddit


def get_hot_news(n_posts=10):
    """
    Obtém os posts mais populares (hot) do subreddit 'news' e retorna uma lista contendo
    informações relevantes de cada post.

    Parâmetros:
        n_posts (int): Número máximo de posts a serem retornados. Valor padrão é 10.

    Retorna:
        list: Uma lista de dicionários, onde cada dicionário possui as seguintes chaves:
              - 'title': título do post.
              - 'url': URL do post.
              - 'score': pontuação do post.
              - 'text': conteúdo textual do post, se disponível.
              - 'comments': número de comentários no post.
    """
    reddit = get_reddit_client()
    subreddit = reddit.subreddit("news")
    posts_response = subreddit.hot(limit=n_posts)
    return [
        {
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "text": post.selftext,
            "comments": post.num_comments,
        }
        for post in posts_response
    ]


def search_posts_by_text(search_text, n_posts=10, llm_option="o1-mini"):
    """
    Retorna uma lista de posts do Reddit baseados na consulta de texto fornecida.
    Parâmetros:
        search_text (str): Texto utilizado para realizar a pesquisa dos posts no subreddit "all".
    Retorna:
        list: Uma lista de dicionários, onde cada dicionário contém os seguintes dados do post:
            - "title": Título do post.
            - "url": URL do post.
            - "score": Pontuação do post.
            - "text": Conteúdo textual do post.
            - "comments": Número de comentários do post.
    Observação:
        A função utiliza a biblioteca 'praw' para se conectar à API do Reddit em modo somente leitura.
    """
    reddit = get_reddit_client()
    subreddit = reddit.subreddit("all")
    posts_response = subreddit.search(search_text, limit=n_posts, sort="hot")

    return [
        {
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "text": post.selftext,
            "comments": post.num_comments,
            "sentiment": classify_sentiment(
                f"{post.title}\n{post.selftext}", llm_option
            ),
            "keywords": get_keyword(f"{post.title}\n{post.selftext}", llm_option),
        }
        for post in posts_response
    ]
