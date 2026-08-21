"""Smoke tests for the Streamlit workout planner interface."""

from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_FILE = Path(__file__).parents[1] / "streamlit_app.py"


def test_streamlit_app_renders_structured_workout_form() -> None:
    app = AppTest.from_file(str(APP_FILE)).run()

    assert not app.exception
    assert [widget.label for widget in app.selectbox] == [
        "🎯 Fitness goal",
        "📈 Experience level",
        "🏠 Equipment access",
    ]
    assert app.slider[0].label == "📅 Days available per week"
    assert app.text_area[0].label == "🛡️ Injuries or limitations (optional)"
    assert app.button[0].label == "Generate my workout plan →"
