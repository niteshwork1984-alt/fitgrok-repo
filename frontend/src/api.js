const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function createWorkoutPlan(request) {
  let response;

  try {
    response = await fetch(`${API_URL}/workout-plan`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch {
    throw new Error(
      "Could not reach the workout service. Make sure the backend is running.",
    );
  }

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      payload.detail || "The workout plan could not be generated. Please try again.",
    );
  }

  if (typeof payload.plan !== "string" || !payload.plan.trim()) {
    throw new Error("The workout service returned an empty plan. Please try again.");
  }

  return payload.plan.trim();
}
