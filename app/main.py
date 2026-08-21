"""FastAPI entry point for the FitGrok backend."""

import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Body, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

from app.models import WorkoutPlanRequest, WorkoutPlanResponse
from app.workout_service import WorkoutGenerationError, WorkoutService


load_dotenv()

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
DEFAULT_FRONTEND_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", DEFAULT_FRONTEND_ORIGINS).split(",")
    if origin.strip()
]

app = FastAPI(
    title="FitGrok API",
    description="Generate personalized workout plans with Groq.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Accept", "Content-Type"],
)


def create_workout_service() -> WorkoutService:
    """Create the workout service from environment configuration."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The server is missing its Groq API configuration.",
        )

    model_name = os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL).strip()
    if not model_name:
        model_name = DEFAULT_GROQ_MODEL

    return WorkoutService(
        client=Groq(api_key=api_key),
        model_name=model_name,
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    """Report whether the HTTP application is running."""
    return {"status": "ok"}


@app.post(
    "/workout-plan",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_200_OK,
)
def generate_workout_plan(
    request: Annotated[
        WorkoutPlanRequest,
        Body(
            openapi_examples={
                "default": {
                    "summary": "Workout plan request",
                    "value": {
                        "fitness_goal": "Build muscle",
                        "experience_level": "Beginner",
                        "days_per_week": 3,
                        "equipment": "Home dumbbells",
                    },
                }
            }
        ),
    ],
) -> WorkoutPlanResponse:
    """Generate a workout plan from structured user input."""
    service = create_workout_service()

    try:
        return service.generate_plan(request)
    except WorkoutGenerationError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
