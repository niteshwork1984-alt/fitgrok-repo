"""Tests for workout plan generation through Groq."""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from groq import APIError

from app.models import (
    EquipmentAccess,
    ExperienceLevel,
    FitnessGoal,
    WorkoutPlanRequest,
)
from app.prompt_builder import SYSTEM_PROMPT
from app.workout_service import WorkoutGenerationError, WorkoutService


@pytest.fixture
def workout_request() -> WorkoutPlanRequest:
    return WorkoutPlanRequest(
        fitness_goal=FitnessGoal.BUILD_MUSCLE,
        experience_level=ExperienceLevel.BEGINNER,
        days_per_week=3,
        equipment=EquipmentAccess.HOME_DUMBBELLS,
    )


def test_generate_plan_returns_trimmed_response(
    workout_request: WorkoutPlanRequest,
) -> None:
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="  ## Plan\n  "))]
    )
    service = WorkoutService(client=client, model_name="test-model")

    response = service.generate_plan(workout_request)

    assert response.plan == "## Plan"
    call_arguments = client.chat.completions.create.call_args.kwargs
    assert call_arguments["model"] == "test-model"
    assert call_arguments["messages"][0] == {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
    assert call_arguments["messages"][1]["role"] == "user"
    assert '"days_per_week": 3' in call_arguments["messages"][1]["content"]


def test_generate_plan_wraps_api_failure(
    workout_request: WorkoutPlanRequest,
) -> None:
    client = MagicMock()
    client.chat.completions.create.side_effect = APIError(
        "network details",
        request=MagicMock(),
        body=None,
    )
    service = WorkoutService(client=client, model_name="test-model")

    with pytest.raises(
        WorkoutGenerationError,
        match="temporarily unavailable",
    ):
        service.generate_plan(workout_request)


def test_generate_plan_rejects_malformed_response(
    workout_request: WorkoutPlanRequest,
) -> None:
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(choices=[])
    service = WorkoutService(client=client, model_name="test-model")

    with pytest.raises(WorkoutGenerationError, match="invalid response"):
        service.generate_plan(workout_request)


def test_generate_plan_rejects_empty_content(
    workout_request: WorkoutPlanRequest,
) -> None:
    client = MagicMock()
    client.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="   "))]
    )
    service = WorkoutService(client=client, model_name="test-model")

    with pytest.raises(WorkoutGenerationError, match="empty response"):
        service.generate_plan(workout_request)


def test_service_rejects_empty_model_name() -> None:
    with pytest.raises(ValueError, match="model name must not be empty"):
        WorkoutService(client=MagicMock(), model_name="   ")
