import os
from groq import Groq
from openai import OpenAI


llm_clients = {
    "o1-mini": OpenAI(api_key=os.environ.get("OPENAI_API_KEY")),
    "deepseek-r1-distill-llama-70b-specdec": Groq(
        api_key=os.environ.get("GROC_API_KEY")
    ),
    "llama-3.1-8b-instant": Groq(api_key=os.environ.get("GROC_API_KEY")),
    "llama-3.3-70b-versatile": Groq(api_key=os.environ.get("GROC_API_KEY")),
}


def classify_sentiment(text, llm_option="o1-mini"):
    """
    Classifica o sentimento de um texto utilizando um modelo de linguagem.

    Parâmetros:
        text (str): Texto que será analisado para determinar seu sentimento.

    Retorna:
        str: Um dos valores 'Positivo', 'Neutro' ou 'Negativo', correspondendo ao sentimento detectado.

    Exceções:
        Poderão ser lançadas exceções relacionadas à comunicação com a API do OpenAI.
    """

    completion = llm_clients[llm_option].chat.completions.create(
        model=llm_option,
        messages=[
            {
                "role": "user",
                "content": f"Classifique o sentimento do texto entre <text> em 'Positivo', 'Neutro' ou 'Negativo', retorne apenas uma dessas opções: <text>{text}</text>",
            },
        ],
    )
    return completion.choices[0].message.content


def summarize_news(posts, llm_option="o1-mini"):
    """
    Gera um resumo em poucas linhas a partir de uma lista de notícias.

    Parâmetros:
        posts (list): Lista de dicionários, onde cada dicionário representa uma notícia com as chaves 'title' e 'text'.

    Retorna:
        str: Resumo gerado pelo modelo de linguagem, combinando os títulos e textos das notícias.
    """
    text = "\n".join([f"{post['title']}: {post['text']}" for post in posts])
    completion = llm_clients[llm_option].chat.completions.create(
        model=llm_option,
        messages=[
            {
                "role": "user",
                "content": f"Interprete as noticias entre <text> e faça um resumo em poucas linhas <text>{text}</text>",
            },
        ],
    )
    return completion.choices[0].message.content


def get_keyword(text, llm_option="o1-mini"):
    """
    Extrai as principais palavras-chave de um texto utilizando o modelo "o1-mini" da API OpenAI.

    Parâmetros:
        text (str): Texto de entrada que será encapsulado entre as tags <text> e </text> para extração das palavras-chave.

    Retorna:
        str: Uma string contendo as principais palavras-chave extraídas do texto.
    """
    completion = llm_clients[llm_option].chat.completions.create(
        model=llm_option,
        messages=[
            {
                "role": "user",
                "content": f"extraia as principais palavras-chaves do texto entre a tag <text> muito resumidamente, retorne apenas uma string: <text>{text}</text>",
            },
        ],
    )
    return completion.choices[0].message.content
