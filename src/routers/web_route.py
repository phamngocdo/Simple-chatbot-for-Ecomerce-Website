from pathlib import Path
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

web_router = APIRouter()

SRC_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=SRC_DIR / "templates")


@web_router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@web_router.get("/chat")
def chat_page(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse("chat.html", {"request": request, "user": user})
