"""Streamlit user interface for generating personalized workout plans."""

import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from app.models import (
    EquipmentAccess,
    ExperienceLevel,
    FitnessGoal,
    WorkoutPlanRequest,
    WorkoutPlanResponse,
)
from app.workout_service import WorkoutGenerationError, WorkoutService


load_dotenv()

DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"


def generate_workout_plan(
    fitness_goal: FitnessGoal,
    experience_level: ExperienceLevel,
    days_per_week: int,
    equipment: EquipmentAccess,
    limitations: str | None = None,
) -> WorkoutPlanResponse:
    """Build a validated request and generate a workout plan through Groq."""
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise WorkoutGenerationError(
                "The Groq API key is missing. Add GROQ_API_KEY to the .env file."
            )

        request = WorkoutPlanRequest(
            fitness_goal=fitness_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            equipment=equipment,
            limitations=limitations,
        )
        service = WorkoutService(
            client=Groq(api_key=api_key),
            model_name=os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL),
        )
        return service.generate_plan(request)
    except WorkoutGenerationError:
        raise
    except Exception as error:
        raise WorkoutGenerationError(
            "The workout plan could not be prepared. Please check the inputs and try again."
        ) from error


def render_page() -> None:
    """Render the complete single-page Streamlit application."""
    st.set_page_config(
        page_title="FitGrok | AI Workout Planner",
        page_icon="🏋️",
        layout="wide",
    )

    st.markdown(
        """
        <style>
            :root {
                --fitgrok-ink: #111320;
                --fitgrok-coral: #ff4d6d;
                --fitgrok-yellow: #ffd43b;
                --fitgrok-blue: #6676ff;
                --fitgrok-paper: #f8f7f2;
            }

            .stApp {
                background:
                    radial-gradient(circle at 8% 8%, rgba(102,118,255,.23), transparent 28%),
                    radial-gradient(circle at 92% 16%, rgba(255,77,109,.18), transparent 25%),
                    #090b14;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            .block-container {
                max-width: 1120px;
                padding-top: 2rem;
                padding-bottom: 4rem;
            }

            .fitgrok-brand {
                display: inline-flex;
                align-items: center;
                gap: .75rem;
                margin-bottom: 3.2rem;
                color: white;
                font-size: 1.15rem;
                font-weight: 900;
                letter-spacing: .13em;
            }

            .fitgrok-logo {
                display: grid;
                width: 48px;
                height: 48px;
                place-items: center;
                color: var(--fitgrok-ink);
                background: var(--fitgrok-yellow);
                border: 2px solid white;
                border-radius: 15px 7px;
                box-shadow: 6px 6px 0 var(--fitgrok-coral);
                font-size: 1.45rem;
            }

            .hero-kicker {
                color: var(--fitgrok-yellow);
                font-size: .78rem;
                font-weight: 900;
                letter-spacing: .15em;
            }

            .hero-title {
                max-width: 820px;
                margin: .7rem 0 1rem;
                color: white;
                font-size: clamp(3rem, 7vw, 6rem);
                font-weight: 950;
                letter-spacing: -.055em;
                line-height: .94;
            }

            .hero-title span {
                color: var(--fitgrok-coral);
            }

            .hero-copy {
                max-width: 700px;
                margin-bottom: 2.6rem;
                color: #bec3d4;
                font-size: 1.08rem;
                line-height: 1.7;
            }

            [data-testid="stForm"] {
                padding: 1.75rem;
                background: var(--fitgrok-paper);
                border: 2px solid white;
                border-radius: 26px 10px;
                box-shadow: 12px 12px 0 var(--fitgrok-blue);
            }

            [data-testid="stForm"] label,
            [data-testid="stForm"] label p {
                color: #242638;
                font-weight: 750;
            }

            [data-testid="stFormSubmitButton"] button,
            [data-testid="stFormSubmitButton"] button p {
                min-height: 3.4rem;
                color: white !important;
                background: var(--fitgrok-ink);
                border: 0;
                border-radius: 10px;
                box-shadow: 0 7px 0 var(--fitgrok-coral);
                font-weight: 900;
            }

            [data-testid="stFormSubmitButton"] button:hover {
                color: white;
                background: #272b45;
                border: 0;
            }

            .result-heading {
                margin: 4rem 0 1.2rem;
                color: var(--fitgrok-yellow);
                font-size: .78rem;
                font-weight: 900;
                letter-spacing: .14em;
            }

            .st-key-plan_output {
                padding: 1.5rem 1.6rem 1.2rem;
                color: #171825;
                background: var(--fitgrok-paper);
                border-radius: 24px 9px;
                box-shadow: 10px 10px 0 var(--fitgrok-yellow);
            }

            .plan-title {
                margin-bottom: 1.4rem;
                color: #171825;
                font-size: 2rem;
                font-weight: 900;
            }

            .st-key-plan_output [data-testid="stMarkdownContainer"],
            .st-key-plan_output [data-testid="stMarkdownContainer"] p,
            .st-key-plan_output [data-testid="stMarkdownContainer"] li,
            .st-key-plan_output [data-testid="stMarkdownContainer"] h1,
            .st-key-plan_output [data-testid="stMarkdownContainer"] h2,
            .st-key-plan_output [data-testid="stMarkdownContainer"] h3,
            .st-key-plan_output [data-testid="stMarkdownContainer"] h4,
            .st-key-plan_output [data-testid="stMarkdownContainer"] strong {
                color: #292c3a !important;
            }

            .st-key-plan_output [data-testid="stMarkdownContainer"] h1,
            .st-key-plan_output [data-testid="stMarkdownContainer"] h2 {
                margin-top: 1.7rem;
            }

            .st-key-plan_output [data-testid="stMarkdownContainer"] table {
                width: 100%;
            }

            .st-key-plan_output [data-testid="stMarkdownContainer"] th {
                color: white !important;
                background: #171a2b;
            }

            .st-key-plan_output [data-testid="stMarkdownContainer"] td {
                color: #292c3a !important;
                background: white;
            }

            .st-key-plan_output [data-testid="stMarkdownContainer"] hr {
                border-color: #d5d7df;
            }

            [data-testid="stDownloadButton"] button,
            [data-testid="stDownloadButton"] button p {
                color: #111320 !important;
                background: var(--fitgrok-yellow);
                border: 0;
                font-weight: 850;
            }

            .fitgrok-footer {
                margin-top: 4rem;
                padding-top: 1.4rem;
                color: #8e94aa;
                border-top: 1px solid #292d42;
                font-size: .82rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="fitgrok-brand">
            <span class="fitgrok-logo">🏋️</span>
            <span>FITGROK</span>
        </div>
        <div class="hero-kicker">⚡ TRAIN WITH INTENTION</div>
        <h1 class="hero-title">YOUR GOALS.<br><span>YOUR PLAN.</span></h1>
        <p class="hero-copy">
            Build a practical weekly workout around your experience, schedule,
            available equipment, and real-world limitations.
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.form("workout_plan_form"):
        goal_column, experience_column = st.columns(2)
        with goal_column:
            fitness_goal = st.selectbox(
                "🎯 Fitness goal",
                options=list(FitnessGoal),
                format_func=lambda option: option.value,
            )
        with experience_column:
            experience_level = st.selectbox(
                "📈 Experience level",
                options=list(ExperienceLevel),
                format_func=lambda option: option.value,
            )

        schedule_column, equipment_column = st.columns(2)
        with schedule_column:
            days_per_week = st.slider(
                "📅 Days available per week",
                min_value=1,
                max_value=7,
                value=3,
            )
        with equipment_column:
            equipment = st.selectbox(
                "🏠 Equipment access",
                options=list(EquipmentAccess),
                format_func=lambda option: option.value,
            )

        limitations = st.text_area(
            "🛡️ Injuries or limitations (optional)",
            placeholder="Example: bad knees or no overhead pressing",
            max_chars=500,
        )
        submitted = st.form_submit_button(
            "Generate my workout plan →",
            use_container_width=True,
        )

    if submitted:
        try:
            with st.spinner("Building your personalized workout plan..."):
                response = generate_workout_plan(
                    fitness_goal=fitness_goal,
                    experience_level=experience_level,
                    days_per_week=days_per_week,
                    equipment=equipment,
                    limitations=limitations.strip() or None,
                )
            st.session_state["workout_plan"] = response.plan
        except WorkoutGenerationError as error:
            st.error(str(error))

    plan = st.session_state.get("workout_plan")
    if plan:
        st.markdown(
            '<div class="result-heading">YOUR CUSTOM PROGRAM</div>',
            unsafe_allow_html=True,
        )
        with st.container(key="plan_output"):
            st.markdown(
                '<div class="plan-title">READY. SET. GROK.</div>',
                unsafe_allow_html=True,
            )
            st.markdown(plan)
        st.download_button(
            "Download plan as Markdown",
            data=plan,
            file_name="fitgrok-workout-plan.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown(
        '<div class="fitgrok-footer">'
        "AI-generated fitness guidance for educational use. Train within your limits."
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    render_page()
