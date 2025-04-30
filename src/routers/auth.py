import os
from dotenv import load_dotenv

from pathlib import Path
from fastapi import APIRouter, Request, Depends, HTTPException,Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from authlib.jose import jwt
import requests

from config.db_config import get_mysql_db as get_db
from services.auth_services import AuthService

SRC_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_uri': 'http://localhost:3000/auth/google/callback'
    }
)

templates = Jinja2Templates(directory=SRC_DIR / "templates")

auth_router = APIRouter()

@auth_router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user_data = {
            "email": email,
            "password": password
        }
        auth_result = await AuthService.login(db=db, user_data=user_data)

        request.session["user"] = auth_result["user"]

        response = RedirectResponse(url="/chat", status_code=302)
        response.set_cookie(key="access_token", value=auth_result["access_token"], httponly=True)
        return response

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@auth_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.get("/google")
async def login_with_google(request: Request, db: Session = Depends(get_db)): 
    redirect_uri = request.url_for('login_with_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_router.get("/google/callback")
async def login_with_google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)

        jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
        jwks = requests.get(jwks_url).json()

        claims = jwt.decode(token['id_token'], jwks)
        claims.validate()

        email = claims.get('email')
        if not email:
            raise HTTPException(status_code=400, detail="Email not found from Google")
        
        auth_result = await AuthService.login_with_google(db=db, email=email)

        response = RedirectResponse(url="/chat", status_code=302)
        response.set_cookie(key="access_token", value=auth_result["access_token"], httponly=True)
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@auth_router.post("/register")
async def register(
    username: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user_data = {
            "username": username,
            "email": email,
            "phone": phone,
            "password": password
        }
        await AuthService.register(db=db, user_data=user_data)

        return RedirectResponse(url="/auth/login", status_code=302)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@auth_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@auth_router.post("/logout")
async def logout(request: Request):
    try:
        if "user" in request.session:
            del request.session["user"]

        response = RedirectResponse(url="/auth/login", status_code=302)
        response.delete_cookie(key="access_token", path="/", httponly=True)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

