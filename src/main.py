import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from starlette.middleware.sessions import SessionMiddleware

from routers.users_route import users_router
from routers.products_route import products_router
from routers.reviews_route import reviews_router
from routers.chat_route import chat_router
from routers.auth_route import auth_router
from routers.web_route import web_router

from chat_model.llm_chatbot import LlmChatBot

SRC_DIR = Path(__file__).resolve().parent

load_dotenv() 

app = FastAPI()

app.mount("/static", StaticFiles(directory=SRC_DIR / "static"), name="static")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(web_router, prefix="", tags=["Web"])

def start():
    port = int(os.getenv("CHAT_PORT", 3000))
    uvicorn.run(
        "main:app",
        host="localhost",
        port=port,
        reload=True,
        reload_dirs=[str(SRC_DIR)]
    )

if __name__ == "__main__":
    start()

