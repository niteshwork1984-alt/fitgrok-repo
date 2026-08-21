import { useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  CalendarDays,
  CheckCircle2,
  Dumbbell,
  Gauge,
  ShieldAlert,
  Sparkles,
  Target,
  Trophy,
  Zap,
} from "lucide-react";
import ReactMarkdown from "react-markdown";

import { createWorkoutPlan } from "./api";

const initialForm = {
  fitness_goal: "Build muscle",
  experience_level: "Beginner",
  days_per_week: 3,
  equipment: "No equipment",
  limitations: "",
};

function App() {
  const [form, setForm] = useState(initialForm);
  const [plan, setPlan] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const resultRef = useRef(null);

  useEffect(() => {
    if (plan || error) {
      resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [plan, error]);

  function updateField(event) {
    const { name, value } = event.target;
    setForm((current) => ({
      ...current,
      [name]: name === "days_per_week" ? Number(value) : value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setPlan("");
    setIsLoading(true);

    try {
      const request = {
        ...form,
        limitations: form.limitations.trim() || null,
      };
      setPlan(await createWorkoutPlan(request));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="site-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="FitGrok home">
          <span className="brand-mark" aria-hidden="true">
            <Dumbbell size={24} strokeWidth={2.8} />
          </span>
          <span>FITGROK</span>
        </a>
        <div className="topbar-tag">
          <span className="status-dot" />
          AI workout engine
        </div>
      </header>

      <main id="top">
        <section className="hero-grid" aria-labelledby="hero-title">
          <div className="hero-copy">
            <div className="eyebrow">
              <Zap size={16} fill="currentColor" />
              TRAIN WITH INTENTION
            </div>
            <h1 id="hero-title">
              YOUR GOALS.
              <span>YOUR PLAN.</span>
            </h1>
            <p className="hero-summary">
              Build a focused weekly workout around your experience, schedule,
              equipment, and real-world limitations.
            </p>

            <div className="process-strip" aria-label="How FitGrok works">
              <div>
                <span>01</span>
                Tell us your goal
              </div>
              <ArrowRight aria-hidden="true" />
              <div>
                <span>02</span>
                Add your constraints
              </div>
              <ArrowRight aria-hidden="true" />
              <div>
                <span>03</span>
                Get your plan
              </div>
            </div>

            <div className="hero-stats">
              <div>
                <Trophy size={22} />
                <strong>Goal-led</strong>
                <span>Built around your target</span>
              </div>
              <div>
                <CheckCircle2 size={22} />
                <strong>Constraint-aware</strong>
                <span>Schedule and gear respected</span>
              </div>
            </div>
          </div>

          <section className="planner-card" aria-labelledby="planner-heading">
            <div className="card-heading">
              <div>
                <span className="section-kicker">BUILD YOUR WEEK</span>
                <h2 id="planner-heading">Plan inputs</h2>
              </div>
              <span className="spark-icon" aria-hidden="true">
                <Sparkles size={22} />
              </span>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="field-grid">
                <label className="field">
                  <span>
                    <Target size={17} /> Fitness goal
                  </span>
                  <select
                    name="fitness_goal"
                    value={form.fitness_goal}
                    onChange={updateField}
                  >
                    <option>Build muscle</option>
                    <option>Lose fat</option>
                    <option>General fitness</option>
                    <option>Improve endurance</option>
                  </select>
                </label>

                <label className="field">
                  <span>
                    <Gauge size={17} /> Experience
                  </span>
                  <select
                    name="experience_level"
                    value={form.experience_level}
                    onChange={updateField}
                  >
                    <option>Beginner</option>
                    <option>Intermediate</option>
                    <option>Advanced</option>
                  </select>
                </label>
              </div>

              <label className="field range-field">
                <span>
                  <CalendarDays size={17} /> Days available
                  <strong>{form.days_per_week} days</strong>
                </span>
                <input
                  type="range"
                  name="days_per_week"
                  min="1"
                  max="7"
                  value={form.days_per_week}
                  onChange={updateField}
                />
                <span className="range-labels" aria-hidden="true">
                  <span>1 day</span>
                  <span>7 days</span>
                </span>
              </label>

              <label className="field">
                <span>
                  <Dumbbell size={17} /> Equipment access
                </span>
                <select
                  name="equipment"
                  value={form.equipment}
                  onChange={updateField}
                >
                  <option>No equipment</option>
                  <option>Home dumbbells</option>
                  <option>Full gym</option>
                </select>
              </label>

              <label className="field">
                <span>
                  <ShieldAlert size={17} /> Injuries or limitations
                  <em>Optional</em>
                </span>
                <textarea
                  name="limitations"
                  value={form.limitations}
                  onChange={updateField}
                  maxLength="500"
                  rows="3"
                  placeholder="Example: bad knees or no overhead pressing"
                />
              </label>

              <button className="generate-button" type="submit" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <span className="button-spinner" /> Building your plan...
                  </>
                ) : (
                  <>
                    Generate my plan <ArrowRight size={20} />
                  </>
                )}
              </button>
            </form>
          </section>
        </section>

        <section
          className={`result-section ${plan || error ? "is-visible" : ""}`}
          ref={resultRef}
          aria-live="polite"
        >
          {error && (
            <div className="error-card" role="alert">
              <ShieldAlert size={26} />
              <div>
                <strong>We hit a snag</strong>
                <p>{error}</p>
              </div>
            </div>
          )}

          {plan && (
            <article className="plan-card">
              <div className="plan-header">
                <div>
                  <span className="section-kicker">YOUR CUSTOM PROGRAM</span>
                  <h2>Ready. Set. Grok.</h2>
                </div>
                <span className="plan-badge">
                  <CheckCircle2 size={16} /> Plan ready
                </span>
              </div>
              <div className="markdown-plan">
                <ReactMarkdown>{plan}</ReactMarkdown>
              </div>
            </article>
          )}
        </section>
      </main>

      <footer>
        <span>FITGROK</span>
        <p>AI-generated guidance for educational use. Train within your limits.</p>
      </footer>
    </div>
  );
}

export default App;
