import httpx
import json
from fastapi import status, HTTPException

from config import settings

SYSTEM_PROMPT = """
You are an expert product tag generator. Given a product name and description,
your task is to generate a concise list of 3 to 5 relevant tags.
The tags should be lowercase, single-word or two-word phrases.
You must respond ONLY with a valid JSON array of strings, like ["tag1", "tag2", "tag3"].
Do not include any other text, explanations, or markdown formatting.
"""


class TagGeneratorService:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self.api_url = f"{settings.OLLAMA_BASE_URL}/api/generate"

    async def generate_tags(self, name: str, description: str) -> list[str]:
        user_prompt = f"Product Name: {name}\nProduct Description: {description}"

        payload = {
            "model": settings.OLLAMA_MODEL,
            "system": SYSTEM_PROMPT,
            "prompt": user_prompt,
            "format": "json",
            "stream": False,
        }

        try:
            response = await self.client.post(self.api_url, json=payload, timeout=60.0)
            response.raise_for_status()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error connecting to Ollama service: {e}",
            )

        try:
            api_data = response.json()
            json_string = api_data.get("response", "[]")
            tags = json.loads(json_string)
            if not isinstance(tags, list) or not all(
                isinstance(tag, str) for tag in tags
            ):
                raise ValueError("LLM returned data in an invalid format.")
            return tags
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to parse response from LLM: {e}",
            )