import os
import uvicorn

from fastapi import FastAPI
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routes.auth import auth_router
from routes.users import users_router
from routes.products import products_router
from routes.reviews import reviews_router
from routes.chat import chat_router
from routes.web import web_router

from chat_model.llm_chatbot import LlmChatBot

templates = Jinja2Templates(directory="src/templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(products_router, prefix="/api/products", tags=["Products"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

app.include_router(web_router, prefix="", tags=["Web"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


def start():
    port = int(os.getenv("CHAT_PORT", 3000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    chatbot = LlmChatBot()
    start()