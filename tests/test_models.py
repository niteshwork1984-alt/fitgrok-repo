"""Tests for the workout plan API models."""

import pytest
from pydantic import ValidationError

from app.models import (
    EquipmentAccess,
    ExperienceLevel,
    FitnessGoal,
    WorkoutPlanRequest,
)


def test_workout_plan_request_accepts_valid_input() -> None:
    request = WorkoutPlanRequest(
        fitness_goal=FitnessGoal.BUILD_MUSCLE,
        experience_level=ExperienceLevel.BEGINNER,
        days_per_week=3,
        equipment=EquipmentAccess.HOME_DUMBBELLS,
        limitations="Bad knees",
    )

    assert request.days_per_week == 3
    assert request.limitations == "Bad knees"


@pytest.mark.parametrize("days_per_week", [0, 8])
def test_workout_plan_request_rejects_invalid_days(days_per_week: int) -> None:
    with pytest.raises(ValidationError):
        WorkoutPlanRequest(
            fitness_goal=FitnessGoal.GENERAL_FITNESS,
            experience_level=ExperienceLevel.INTERMEDIATE,
            days_per_week=days_per_week,
            equipment=EquipmentAccess.NO_EQUIPMENT,
        )


def test_workout_plan_request_converts_blank_limitations_to_none() -> None:
    request = WorkoutPlanRequest(
        fitness_goal=FitnessGoal.IMPROVE_ENDURANCE,
        experience_level=ExperienceLevel.ADVANCED,
        days_per_week=5,
        equipment=EquipmentAccess.FULL_GYM,
        limitations="   ",
    )

    assert request.limitations is None


def test_workout_plan_request_rejects_unknown_goal() -> None:
    with pytest.raises(ValidationError):
        WorkoutPlanRequest(
            fitness_goal="Become invincible",
            experience_level=ExperienceLevel.BEGINNER,
            days_per_week=2,
            equipment=EquipmentAccess.NO_EQUIPMENT,
        )
