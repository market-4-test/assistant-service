from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, Depends, HTTPException, status

import schemas
import services
from services import TagGeneratorService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()
    yield
    await app.state.http_client.aclose()


app = FastAPI(
    title="Assistant Service",
    description="Service for suggesting product tags using a local LLM.",
    version="1.0.0",
    lifespan=lifespan,
)


def get_tag_generator_service(
    client: httpx.AsyncClient = Depends(lambda app: app.state.http_client)
) -> TagGeneratorService:
    return TagGeneratorService(client=client)


@app.get("/", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check():
    return {"status": "ok"}


@app.post(
    "/suggest-tags",
    response_model=schemas.TagSuggestionResponse,
    status_code=status.HTTP_200_OK,
    tags=["AI"],
)
async def suggest_tags(
    request: schemas.TagSuggestionRequest,
    tag_service: TagGeneratorService = Depends(get_tag_generator_service),
):
    """
    Generates a list of suggested tags based on product name and description.
    """
    suggested_tags = await tag_service.generate_tags(
        name=request.name, description=request.description
    )
    return schemas.TagSuggestionResponse(suggestedTags=suggested_tags)