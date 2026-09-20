"use client";

import {
  CircleAlert,
  Dumbbell,
  RefreshCw,
  Salad,
  Save,
  UserRound,
} from "lucide-react";
import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import {
  ApiError,
  getCurrentUser,
  type CurrentUser,
  updateCurrentUser,
} from "@/lib/api";

const activityOptions = [
  ["sedentary", "Sedentary"],
  ["light", "Lightly active"],
  ["moderate", "Moderately active"],
  ["active", "Active"],
  ["very_active", "Very active"],
  ["extra_active", "Extra active"],
] as const;

const goalOptions = [
  ["weight_loss", "Weight loss"],
  ["weight_gain", "Weight gain"],
  ["muscle_gain", "Muscle gain"],
  ["maintenance", "Maintain weight"],
] as const;

const dietaryOptions = [
  "balanced",
  "vegetarian",
  "vegan",
  "high_protein",
  "low_carb",
] as const;

const workoutOptions = [
  ["home", "At home"],
  ["gym", "At a gym"],
  ["mixed", "Home and gym"],
] as const;

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [sex, setSex] = useState("");
  const [goal, setGoal] = useState("weight_loss");
  const [activity, setActivity] = useState("moderate");
  const [dietaryPreference, setDietaryPreference] = useState("balanced");
  const [workoutPreference, setWorkoutPreference] = useState("home");
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  function populateForm(profile: CurrentUser) {
    setFullName(profile.full_name);
    setAge(profile.age ? String(profile.age) : "");
    setHeight(profile.height_cm ? String(profile.height_cm) : "");
    setWeight(profile.weight_kg ? String(profile.weight_kg) : "");
    setSex(profile.sex || "");
    setGoal(profile.fitness_goal || "weight_loss");
    setActivity(profile.activity_level || "moderate");
    setDietaryPreference(profile.dietary_preference || "balanced");
    setWorkoutPreference(profile.workout_preference || "home");
  }

  async function loadProfile(showRefreshState = false) {
    if (showRefreshState) {
      setRefreshing(true);
    }

    setErrorMessage("");

    try {
      const profile = await getCurrentUser();
      setUser(profile);
      populateForm(profile);
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Your profile is not available right now.",
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialProfile() {
      try {
        const profile = await getCurrentUser();
        if (!cancelled) {
          setUser(profile);
          populateForm(profile);
        }
      } catch (error) {
        if (cancelled) {
          return;
        }

        if (error instanceof ApiError && error.status === 401) {
          router.replace("/login");
          return;
        }

        setErrorMessage(
          error instanceof ApiError
            ? error.detail
            : "Your profile is not available right now.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInitialProfile();

    return () => {
      cancelled = true;
    };
  }, [router]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    const ageValue = Number(age);
    const heightValue = Number(height);
    const weightValue = Number(weight);

    if (!fullName.trim() || !ageValue || !heightValue || !weightValue || !sex) {
      setErrorMessage(
        "Enter your name, age, height, weight, and calorie-estimate option to save a complete profile.",
      );
      return;
    }

    setSaving(true);

    try {
      const profile = await updateCurrentUser({
        full_name: fullName.trim(),
        age: ageValue,
        height_cm: heightValue,
        weight_kg: weightValue,
        sex,
        fitness_goal: goal,
        dietary_preference: dietaryPreference,
        activity_level: activity,
        workout_preference: workoutPreference,
      });

      setUser(profile);
      populateForm(profile);
      setSuccessMessage(
        "Profile saved. Your Dietician can now use these details to generate a plan.",
      );
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Unable to save your profile.",
      );
    } finally {
      setSaving(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-5xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="Your account"
          title="Fitness profile"
          description="Save the measurements and goals that personalize your Dietician, planner, and AI recommendations."
          icon={UserRound}
          action={
            <button
              type="button"
              onClick={() => void loadProfile(true)}
              disabled={loading || refreshing || saving}
              className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-zinc-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCw size={16} className={refreshing ? "animate-spin" : ""} />
              {refreshing ? "Refreshing..." : "Refresh profile"}
            </button>
          }
        />

        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/5 p-4 text-sm text-red-300">
            <CircleAlert size={18} className="mt-0.5 shrink-0" />
            <p>{errorMessage}</p>
          </div>
        )}

        {successMessage && (
          <div className="mt-6 rounded-2xl border border-emerald-400/15 bg-emerald-400/5 p-4 text-sm text-emerald-200">
            {successMessage}
          </div>
        )}

        {loading ? (
          <div className="mt-8 h-96 animate-pulse rounded-3xl border border-white/10 bg-white/[0.025]" />
        ) : user ? (
          <section className="mt-8 grid gap-5 lg:grid-cols-[0.72fr_1.28fr]">
            <article className="rounded-3xl border border-cyan-300/15 bg-gradient-to-br from-cyan-400/[0.11] to-[#0b0e13] p-6">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-cyan-400 text-xl font-semibold text-black">
                {(user.full_name[0] ?? "A").toUpperCase()}
              </div>
              <h2 className="mt-5 text-xl font-semibold">{user.full_name}</h2>
              <p className="mt-1 break-all text-sm text-zinc-400">{user.email}</p>
              <span className="mt-5 inline-flex rounded-full border border-emerald-400/15 bg-emerald-400/5 px-3 py-1.5 text-xs text-emerald-300">
                {user.is_active ? "Active account" : "Account paused"}
              </span>
              <p className="mt-6 text-sm leading-6 text-zinc-500">
                Keep these values current for more accurate calorie targets and workout recommendations.
              </p>
            </article>

            <form onSubmit={handleSubmit} className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
              <div>
                <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Personalization details
                </p>
                <h2 className="mt-2 text-xl font-semibold">Complete your profile</h2>
              </div>

              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <label className="block sm:col-span-2">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Full name</span>
                  <input
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                    required
                    minLength={2}
                    className="h-11 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  />
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Age</span>
                  <input
                    value={age}
                    onChange={(event) => setAge(event.target.value)}
                    type="number"
                    min="13"
                    max="120"
                    required
                    className="h-11 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  />
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Dietary preference</span>
                  <select
                    value={dietaryPreference}
                    onChange={(event) => setDietaryPreference(event.target.value)}
                    className="h-11 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  >
                    {dietaryOptions.map((option) => (
                      <option key={option} value={option}>
                        {option.replace(/_/g, " ")}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Sex used for calorie estimates</span>
                  <select
                    value={sex}
                    onChange={(event) => setSex(event.target.value)}
                    required
                    className="h-11 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  >
                    <option value="">Choose an option</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Height (cm)</span>
                  <input
                    value={height}
                    onChange={(event) => setHeight(event.target.value)}
                    type="number"
                    min="1"
                    max="300"
                    required
                    className="h-11 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  />
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Weight (kg)</span>
                  <input
                    value={weight}
                    onChange={(event) => setWeight(event.target.value)}
                    type="number"
                    min="1"
                    max="500"
                    step="0.1"
                    required
                    className="h-11 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  />
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Activity level</span>
                  <select
                    value={activity}
                    onChange={(event) => setActivity(event.target.value)}
                    className="h-11 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  >
                    {activityOptions.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>

                <label className="block">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Fitness goal</span>
                  <select
                    value={goal}
                    onChange={(event) => setGoal(event.target.value)}
                    className="h-11 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  >
                    {goalOptions.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>

                <label className="block sm:col-span-2">
                  <span className="mb-2 block text-sm font-medium text-zinc-300">Workout setting</span>
                  <select
                    value={workoutPreference}
                    onChange={(event) => setWorkoutPreference(event.target.value)}
                    className="h-11 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                  >
                    {workoutOptions.map(([value, label]) => (
                      <option key={value} value={value}>{label}</option>
                    ))}
                  </select>
                </label>
              </div>

              <button
                type="submit"
                disabled={saving}
                className="mt-6 inline-flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-4 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <Save size={16} />
                {saving ? "Saving profile..." : "Save profile"}
              </button>
            </form>
          </section>
        ) : null}

        <section className="mt-5 grid gap-4 sm:grid-cols-2">
          <Link href="/dietician" className="group rounded-2xl border border-white/10 bg-[#0b0e13] p-5 transition hover:border-cyan-300/25 hover:bg-[#0d1117]">
            <Salad size={19} className="text-cyan-300" />
            <h2 className="mt-4 font-semibold">Build a diet plan</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-500">Use the saved profile values to generate your personalized diet plan.</p>
          </Link>
          <Link href="/trainer" className="group rounded-2xl border border-white/10 bg-[#0b0e13] p-5 transition hover:border-cyan-300/25 hover:bg-[#0d1117]">
            <Dumbbell size={19} className="text-cyan-300" />
            <h2 className="mt-4 font-semibold">Analyze a workout</h2>
            <p className="mt-2 text-sm leading-6 text-zinc-500">Upload a recording to receive detailed rep and performance feedback.</p>
          </Link>
        </section>
      </div>
    </main>
  );
}
