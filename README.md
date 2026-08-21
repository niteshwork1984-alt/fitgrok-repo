# FitGrok

FitGrok is a small FastAPI backend that generates personalized workout plans
through the Groq API.

## Backend setup

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then replace the placeholder API key:

```bash
cp .env.example .env
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

The interactive API documentation is available at
`http://127.0.0.1:8000/docs`.

## Generate a workout plan

Send a `POST` request to `/workout-plan`:

```json
{
  "fitness_goal": "Build muscle",
  "experience_level": "Beginner",
  "days_per_week": 3,
  "equipment": "Home dumbbells",
  "limitations": null
}
```

Successful response:

```json
{
  "plan": "## Weekly Workout Plan\n..."
}
```

## Tests

```bash
pytest -q
```
