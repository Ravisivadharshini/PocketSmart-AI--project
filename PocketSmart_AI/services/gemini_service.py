import os
import json

from services.recommendation_service import fallback_recommendations

try:
    from google import genai
except Exception:
    genai = None

def generate_recommendations(category: str, data: dict):
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    if not api_key or genai is None:
        return {
            "source": "fallback",
            "message": "Demo mode: add GEMINI_API_KEY to .env for Gemini-generated recommendations.",
            "recommendations": fallback_recommendations(category, data)
        }

    prompt = f"""
You are PocketSmart AI, a budget-aware recommendation assistant.
Category: {category}
User data:
{json.dumps(data, indent=2)}

Return ONLY valid JSON in this shape:
{{
  "summary": "short summary",
  "recommendations": [
    {{
      "title": "product/service name",
      "platform": "Amazon/Flipkart/IKEA/Swiggy/Zomato/OYO/Other",
      "price": 0,
      "reason": "why it fits"
    }}
  ]
}}
Keep the total suggested spending within the user's budget. Do not claim live prices or live availability.
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model_name, contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(text)
        return {"source": "gemini", **parsed}
    except Exception as exc:
        return {
            "source": "fallback",
            "message": f"Gemini call failed, so demo recommendations are shown: {exc}",
            "recommendations": fallback_recommendations(category, data)
        }
