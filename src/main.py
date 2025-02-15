from fastapi import FastAPI, Depends

from routes.reddit_router import router as reddit_router
from utils_general import common_verificacao_api_token


app = FastAPI(
    title="Reddit Analyzer",
    description="API para analisar dados do Reddit, desenvolvido para a disciplina de APIs da UFG",
    version="0.1",
    dependencies=[Depends(common_verificacao_api_token)],
)

app.include_router(reddit_router, prefix="/reddit")
