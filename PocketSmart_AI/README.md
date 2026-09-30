# PocketSmart AI — Smart Budget & Recommendation Assistant

A FastAPI + Jinja2 project based on the supplied PocketSmart AI project document.

## Included modules
- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional image upload
- Register / Login / Logout
- JWT token endpoint
- Session information endpoints
- Recommendation history with SQLite
- Gemini integration with a safe fallback demo mode
- Responsive HTML/CSS/JavaScript frontend

## Important
The project works in demo/fallback mode without a Gemini API key. To enable Gemini:
1. Copy `.env.example` to `.env`
2. Add your Gemini API key.
3. Set `GEMINI_MODEL` to a model available in your account if `gemini-1.5-flash` is unavailable.

The generated recommendations are examples and do not represent live product prices or live availability.

## Run
### Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app:app --reload
```

Open: http://127.0.0.1:8000
