import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

prompt = """You are a luxury hotel marketing strategist for a 5-star hotel in Dubai (similar to FIVE Hotels).

Context:
- Hotel type: City Hotel
- Week: 2026-06-15
- Predicted occupancy: 50%
- Target occupancy threshold: 65%
- Demand gap: 15% below target
- Urgency level: high

Generate a marketing response package with exactly this JSON structure:
{
  "whatsapp_message": "2-sentence luxury flash deal for UAE residents (max 160 chars)",
  "email_subject": "compelling subject line for a targeted re-engagement email",
  "instagram_caption": "luxury lifestyle caption with 3 relevant hashtags",
  "recommended_discount": "specific % discount or package offer",
  "target_segment": "which guest segment to target (e.g. UAE residents, GCC travelers, business travelers)"
}

Tone: luxury, aspirational, exclusive — never cheap or desperate. Think Ritz-Carlton, not budget hotel."""

resp = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers={'Authorization': 'Bearer ' + os.getenv('OPENROUTER_API_KEY', os.getenv('ANTHROPIC_API_KEY', ''))},
    json={'model': 'minimax/minimax-m3', 'messages': [{'role': 'user', 'content': prompt}]}
)

with open('minimax_out.json', 'w', encoding='utf-8') as f:
    json.dump(resp.json(), f, indent=2)
