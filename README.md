# FitGrok

FitGrok is a small FastAPI backend that generates personalized workout plans
through the Groq API, with a single-page React frontend.

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

## Frontend setup

In a second terminal, install and start the React application:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in a browser. The frontend calls the backend at
`http://127.0.0.1:8000` by default. To use a different backend URL, copy
`frontend/.env.example` to `frontend/.env` and update `VITE_API_URL`.

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
cd frontend
npm test
npm run build
```
