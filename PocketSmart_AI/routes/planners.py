import json
from pathlib import Path

from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from database import add_history, get_history
from models.schemas import HomeRequest, PartyRequest, JewelryRequest
from routes.auth import current_user
from services.gemini_service import generate_recommendations

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def save_and_return(request, category, data, result):
    user = current_user(request)
    if user:
        add_history(user["id"], category, float(data["budget"]), json.dumps(data), json.dumps(result))
    return result

@router.post("/generate-home")
async def generate_home(request: Request, payload: HomeRequest):
    data = payload.model_dump()
    result = generate_recommendations("home", data)
    return save_and_return(request, "Home", data, result)

@router.post("/generate-party")
async def generate_party(request: Request, payload: PartyRequest):
    data = payload.model_dump()
    result = generate_recommendations("party", data)
    return save_and_return(request, "Party", data, result)

@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("Elegant"),
    outfit_color: str = Form(""),
    image: UploadFile | None = File(None)
):
    image_name = None
    if image and image.filename:
        safe_name = Path(image.filename).name.replace(" ", "_")
        image_name = safe_name
        (UPLOAD_DIR / safe_name).write_bytes(await image.read())

    data = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_color=outfit_color or None,
        image_name=image_name
    ).model_dump()

    result = generate_recommendations("jewelry", data)
    return save_and_return(request, "Jewelry", data, result)

@router.get("/recommendations-details", response_class=HTMLResponse)
async def recommendations_details(request: Request):
    return templates.TemplateResponse("recommendations.html", {
        "request": request,
        "result": None
    })

@router.get("/api/history")
async def api_history(request: Request):
    user = current_user(request)
    if not user:
        return JSONResponse({"detail": "Login required"}, status_code=401)
    rows = get_history(user["id"])
    return [
        {
            "id": r["id"], "category": r["category"], "budget": r["budget"],
            "request": json.loads(r["request_json"]),
            "response": json.loads(r["response_json"]),
            "created_at": r["created_at"]
        }
        for r in rows
    ]

@router.get("/api/recommendation")
async def api_recommendation():
    return {"message": "Use /generate-home, /generate-party or /generate-jewelry."}
