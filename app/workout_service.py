"""Service for generating workout plans through the Groq API."""

from groq import APIError, Groq

from app.models import WorkoutPlanRequest, WorkoutPlanResponse
from app.prompt_builder import SYSTEM_PROMPT, build_workout_prompt


class WorkoutGenerationError(RuntimeError):
    """Raised when a workout plan cannot be generated."""


class WorkoutService:
    """Generate workout plans using a configured Groq client."""

    def __init__(self, client: Groq, model_name: str) -> None:
        if not model_name.strip():
            raise ValueError("Groq model name must not be empty.")

        self._client = client
        self._model_name = model_name

    def generate_plan(self, request: WorkoutPlanRequest) -> WorkoutPlanResponse:
        """Generate a workout plan for a validated request."""
        try:
            completion = self._client.chat.completions.create(
                model=self._model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_workout_prompt(request)},
                ],
            )
        except APIError as error:
            raise WorkoutGenerationError(
                "The workout plan service is temporarily unavailable. "
                "Please try again."
            ) from error

        try:
            content = completion.choices[0].message.content
        except (AttributeError, IndexError, TypeError) as error:
            raise WorkoutGenerationError(
                "The workout plan service returned an invalid response. "
                "Please try again."
            ) from error

        if not isinstance(content, str) or not content.strip():
            raise WorkoutGenerationError(
                "The workout plan service returned an empty response. "
                "Please try again."
            )

        return WorkoutPlanResponse(plan=content.strip())
