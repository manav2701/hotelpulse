import anthropic
import os
from dotenv import load_dotenv
load_dotenv()

def generate_marketing_alert(
    predicted_occupancy: float,
    week_label: str,
    hotel_type: str,
    threshold: float = 0.65
) -> dict:
    """
    Called when predicted occupancy drops below threshold.
    Returns generated marketing copy in multiple formats.
    """
    if predicted_occupancy >= threshold:
        return {"triggered": False, "message": None}

    gap = threshold - predicted_occupancy
    urgency = "high" if gap > 0.15 else "medium"

    prompt = f"""You are a luxury hotel marketing strategist for a 5-star hotel in Dubai (similar to FIVE Hotels).

Context:
- Hotel type: {hotel_type}
- Week: {week_label}
- Predicted occupancy: {predicted_occupancy:.0%}
- Target occupancy threshold: {threshold:.0%}
- Demand gap: {gap:.0%} below target
- Urgency level: {urgency}

Generate a marketing response package with exactly this JSON structure:
{{
  "whatsapp_message": "2-sentence luxury flash deal for UAE residents (max 160 chars)",
  "email_subject": "compelling subject line for a targeted re-engagement email",
  "instagram_caption": "luxury lifestyle caption with 3 relevant hashtags",
  "recommended_discount": "specific % discount or package offer",
  "target_segment": "which guest segment to target (e.g. UAE residents, GCC travelers, business travelers)"
}}

Tone: luxury, aspirational, exclusive — never cheap or desperate. Think Ritz-Carlton, not budget hotel."""

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "triggered": True,
            "error": "Missing ANTHROPIC_API_KEY in environment",
        }

    import requests
    import json
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://hotelpulse.local",
        "X-Title": "HotelPulse"
    }
    
    data = {
        "model": "minimax/minimax-m3",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 3000
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=90
        )
        resp_json = response.json()
        if 'error' in resp_json:
            return {"triggered": True, "error": f"OpenRouter API Error: {resp_json['error']}"}
            
        content = resp_json.get('choices', [{}])[0].get('message', {}).get('content')
        if not content:
            return {"triggered": True, "error": "Model returned an empty response or unexpected JSON."}
        # Extract JSON from response
        start = content.find('{')
        end = content.rfind('}') + 1
        result = json.loads(content[start:end])
        result["triggered"] = True
        result["predicted_occupancy"] = predicted_occupancy
        return result
    except Exception as e:
        return {
            "triggered": True,
            "error": str(e)
        }
