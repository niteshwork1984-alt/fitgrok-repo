"""Request and response models for the workout plan API."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class FitnessGoal(str, Enum):
    """Fitness goals supported by the workout generator."""

    BUILD_MUSCLE = "Build muscle"
    LOSE_FAT = "Lose fat"
    GENERAL_FITNESS = "General fitness"
    IMPROVE_ENDURANCE = "Improve endurance"


class ExperienceLevel(str, Enum):
    """Experience levels supported by the workout generator."""

    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class EquipmentAccess(str, Enum):
    """Equipment options supported by the workout generator."""

    NO_EQUIPMENT = "No equipment"
    HOME_DUMBBELLS = "Home dumbbells"
    FULL_GYM = "Full gym"


class WorkoutPlanRequest(BaseModel):
    """Validated user input for generating a workout plan."""

    fitness_goal: FitnessGoal
    experience_level: ExperienceLevel
    days_per_week: int = Field(ge=1, le=7)
    equipment: EquipmentAccess
    limitations: str | None = Field(default=None, max_length=500)

    @field_validator("limitations")
    @classmethod
    def normalize_limitations(cls, value: str | None) -> str | None:
        """Treat an empty limitations value as an omitted value."""
        if value is None:
            return None

        normalized_value = value.strip()
        return normalized_value or None


class WorkoutPlanResponse(BaseModel):
    """Successful response returned by the workout plan API."""

    plan: str = Field(min_length=1)
