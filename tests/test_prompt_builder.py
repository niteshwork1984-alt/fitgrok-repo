"""Tests for workout prompt construction."""

from app.models import (
    EquipmentAccess,
    ExperienceLevel,
    FitnessGoal,
    WorkoutPlanRequest,
)
from app.prompt_builder import SYSTEM_PROMPT, build_workout_prompt


def test_system_prompt_defines_safety_and_constraint_rules() -> None:
    assert "Follow the requested number of training days" in SYSTEM_PROMPT
    assert "available equipment" in SYSTEM_PROMPT
    assert "Do not diagnose conditions or make medical claims" in SYSTEM_PROMPT
    assert "Return clear Markdown" in SYSTEM_PROMPT


def test_prompt_contains_every_structured_input() -> None:
    request = WorkoutPlanRequest(
        fitness_goal=FitnessGoal.BUILD_MUSCLE,
        experience_level=ExperienceLevel.BEGINNER,
        days_per_week=3,
        equipment=EquipmentAccess.HOME_DUMBBELLS,
        limitations="Bad knees",
    )

    prompt = build_workout_prompt(request)

    assert '"fitness_goal": "Build muscle"' in prompt
    assert '"experience_level": "Beginner"' in prompt
    assert '"days_per_week": 3' in prompt
    assert '"equipment": "Home dumbbells"' in prompt
    assert '"limitations": "Bad knees"' in prompt
    assert "exactly 3 training days labeled Day 1 through Day 3" in prompt


def test_prompt_adds_limitation_safety_instruction_when_needed() -> None:
    request = WorkoutPlanRequest(
        fitness_goal=FitnessGoal.GENERAL_FITNESS,
        experience_level=ExperienceLevel.INTERMEDIATE,
        days_per_week=4,
        equipment=EquipmentAccess.FULL_GYM,
        limitations="No overhead pressing",
    )

    prompt = build_workout_prompt(request)

    assert "Adapt exercises around the stated limitations" in prompt
    assert "include a short safety disclaimer" in prompt


def test_prompt_handles_missing_limitations() -> None:
    request = WorkoutPlanRequest(
        fitness_goal=FitnessGoal.IMPROVE_ENDURANCE,
        experience_level=ExperienceLevel.ADVANCED,
        days_per_week=5,
        equipment=EquipmentAccess.NO_EQUIPMENT,
    )

    prompt = build_workout_prompt(request)

    assert '"limitations": "None reported"' in prompt
    assert "No injury-specific disclaimer is required" in prompt
