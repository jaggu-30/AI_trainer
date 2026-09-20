import type { CurrentUser } from "@/lib/api";

export function hasCompletedFitnessSetup(
  user: CurrentUser,
): boolean {
  return Boolean(
    user.age &&
      user.height_cm &&
      user.weight_kg &&
      user.sex &&
      user.fitness_goal &&
      user.dietary_preference &&
      user.activity_level &&
      user.workout_preference,
  );
}

export function profileSetupMessage(): string {
  return "Complete your one-time fitness setup to receive a diet plan, workout plan, and live coaching tailored to you.";
}
