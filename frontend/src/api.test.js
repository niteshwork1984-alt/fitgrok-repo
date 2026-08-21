import { afterEach, describe, expect, it, vi } from "vitest";

import { createWorkoutPlan } from "./api";

describe("createWorkoutPlan", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("returns a generated plan", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ plan: "  # Day 1  " }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const plan = await createWorkoutPlan({ days_per_week: 1 });

    expect(plan).toBe("# Day 1");
    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/workout-plan",
      expect.objectContaining({ method: "POST" }),
    );
  });

  it("uses the API error message", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        json: async () => ({ detail: "Groq is unavailable." }),
      }),
    );

    await expect(createWorkoutPlan({})).rejects.toThrow("Groq is unavailable.");
  });

  it("reports a backend connection failure", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

    await expect(createWorkoutPlan({})).rejects.toThrow(
      "Make sure the backend is running",
    );
  });
});
