import os
from openai import OpenAI

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def classify_sentiment(text):
    completion = openai_client.chat.completions.create(
        model="o1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Classifique o sentimento do texto entre <text> em 'Positivo', 'Neutro' ou 'Negativo', retorne apenas uma dessas opções: <text>{text}</text>",
            },
        ],
    )
    return completion.choices[0].message.content


def summarize_news(posts):
    text = "\n".join([f"{post['title']}: {post['text']}" for post in posts])
    completion = openai_client.chat.completions.create(
        model="o1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Interprete as noticias entre <text> e faça um resumo em poucas linhas <text>{text}</text>",
            },
        ],
    )
    return completion.choices[0].message.content


def get_keyword(text):
    completion = openai_client.chat.completions.create(
        model="o1-mini",
        messages=[
            {
                "role": "user",
                "content": f"extraia as principais palavras-chaves do texto entre a tag <text> muito resumidamente, retorne apenas uma string: <text>{text}</text>",
            },
        ],
    )
    return completion.choices[0].message.content
