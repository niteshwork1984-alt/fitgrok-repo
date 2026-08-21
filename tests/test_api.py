"""Tests for the FitGrok HTTP API."""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.models import WorkoutPlanResponse
from app.workout_service import WorkoutGenerationError


client = TestClient(app)


def valid_request_body() -> dict[str, object]:
    return {
        "fitness_goal": "Build muscle",
        "experience_level": "Beginner",
        "days_per_week": 3,
        "equipment": "Home dumbbells",
        "limitations": None,
    }


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_frontend_origin_can_call_workout_endpoint() -> None:
    response = client.options(
        "/workout-plan",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_openapi_example_omits_missing_limitations() -> None:
    schema = app.openapi()
    request_example = schema["paths"]["/workout-plan"]["post"]["requestBody"][
        "content"
    ]["application/json"]["examples"]["default"]["value"]

    assert "limitations" not in request_example


def test_generate_workout_plan_returns_service_response(monkeypatch) -> None:
    service = MagicMock()
    service.generate_plan.return_value = WorkoutPlanResponse(plan="## Weekly Plan")
    monkeypatch.setattr("app.main.create_workout_service", lambda: service)

    response = client.post("/workout-plan", json=valid_request_body())

    assert response.status_code == 200
    assert response.json() == {"plan": "## Weekly Plan"}
    submitted_request = service.generate_plan.call_args.args[0]
    assert submitted_request.days_per_week == 3


def test_generate_workout_plan_rejects_invalid_input(monkeypatch) -> None:
    service_factory = MagicMock()
    monkeypatch.setattr("app.main.create_workout_service", service_factory)
    request_body = valid_request_body()
    request_body["days_per_week"] = 0

    response = client.post("/workout-plan", json=request_body)

    assert response.status_code == 422
    service_factory.assert_not_called()


def test_generate_workout_plan_maps_service_error(monkeypatch) -> None:
    service = MagicMock()
    service.generate_plan.side_effect = WorkoutGenerationError(
        "The workout plan service is temporarily unavailable. Please try again."
    )
    monkeypatch.setattr("app.main.create_workout_service", lambda: service)

    response = client.post("/workout-plan", json=valid_request_body())

    assert response.status_code == 502
    assert response.json() == {
        "detail": (
            "The workout plan service is temporarily unavailable. Please try again."
        )
    }


def test_generate_workout_plan_reports_missing_api_key(
    monkeypatch,
) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    response = client.post("/workout-plan", json=valid_request_body())

    assert response.status_code == 500
    assert response.json() == {
        "detail": "The server is missing its Groq API configuration."
    }
