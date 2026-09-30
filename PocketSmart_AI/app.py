from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pathlib import Path

from database import init_db
from routes.pages import router as pages_router
from routes.auth import router as auth_router
from routes.planners import router as planners_router

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="PocketSmart AI: Smart Budget Planner", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(planners_router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "PocketSmart AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
