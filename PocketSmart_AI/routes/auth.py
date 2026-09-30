import os
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from jose import jwt

from database import create_user, get_user_by_email, get_user_by_id, verify_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def make_token(user_id: int):
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "exp": exp},
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return get_user_by_id(int(payload["sub"]))
    except Exception:
        return None


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )


@router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)

    if not user or not verify_password(password, user["password_hash"]):
        return RedirectResponse(
            "/login?error=Invalid%20email%20or%20password",
            status_code=303
        )

    token = make_token(user["id"])
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="lax"
    )
    return response


@router.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request}
    )


@router.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        create_user(name, email, password)
    except Exception:
        return RedirectResponse(
            "/register?error=Email%20already%20registered",
            status_code=303
        )

    return RedirectResponse("/login?registered=1", status_code=303)


@router.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response


@router.get("/token")
async def token(request: Request):
    user = current_user(request)

    if not user:
        return JSONResponse(
            {"detail": "Not authenticated"},
            status_code=401
        )

    return {
        "access_token": make_token(user["id"]),
        "token_type": "bearer"
    }


@router.get("/session-info")
async def session_info(request: Request):
    user = current_user(request)

    if not user:
        return {"authenticated": False}

    return {
        "authenticated": True,
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }


@router.get("/session-data")
async def session_data(request: Request):
    user = current_user(request)

    if not user:
        return JSONResponse(
            {"detail": "Not authenticated"},
            status_code=401
        )

    return {
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }