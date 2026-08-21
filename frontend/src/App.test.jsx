import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, expect, it, vi } from "vitest";

import App from "./App";
import { createWorkoutPlan } from "./api";

vi.mock("./api", () => ({
  createWorkoutPlan: vi.fn(),
}));

beforeEach(() => {
  createWorkoutPlan.mockReset();
  window.HTMLElement.prototype.scrollIntoView = vi.fn();
});

it("shows the workout planning form", () => {
  render(<App />);

  expect(screen.getByRole("link", { name: "FitGrok home" })).toBeInTheDocument();
  expect(screen.getByRole("heading", { name: /your goals/i })).toBeInTheDocument();
  expect(screen.getByLabelText(/fitness goal/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/experience/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /generate my plan/i })).toBeInTheDocument();
});

it("submits null when limitations are blank and renders the plan", async () => {
  createWorkoutPlan.mockResolvedValue("# Day 1\n\nA focused workout.");
  render(<App />);

  fireEvent.click(screen.getByRole("button", { name: /generate my plan/i }));

  await waitFor(() => {
    expect(createWorkoutPlan).toHaveBeenCalledWith(
      expect.objectContaining({
        fitness_goal: "Build muscle",
        days_per_week: 3,
        limitations: null,
      }),
    );
  });
  expect(await screen.findByRole("heading", { name: "Day 1" })).toBeInTheDocument();
});
