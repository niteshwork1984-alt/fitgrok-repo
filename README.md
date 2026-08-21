# FitGrok

FitGrok is a single-page Streamlit application that generates personalized
workout plans through the Groq API. It uses structured inputs, typed Python
functions, prompt design, and friendly error handling.

## Required assignment app: Streamlit

Create a virtual environment and install the Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then replace the placeholder API key:

```bash
cp .env.example .env
```

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in a browser.

The Streamlit page collects:

- Fitness goal
- Experience level
- Days available per week
- Equipment access
- Optional injuries or limitations

It displays the generated plan as Markdown and provides a Markdown download
button. The most recently generated plan remains available across Streamlit
reruns through session state.

## Optional FastAPI and React extension

The repository also contains an optional REST API and React interface. They are
not required to run the Streamlit assignment.

Start the FastAPI backend:

```bash
uvicorn app.main:app --reload
```

The interactive API documentation is available at
`http://127.0.0.1:8000/docs`.

## Frontend setup

In a second terminal, install and start the optional React application:

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
```

Optional React checks:

```bash
cd frontend
npm test
npm run build
```
