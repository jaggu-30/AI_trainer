"use client";

import { FormEvent, useEffect, useState } from "react";
import { ArrowRight, CircleAlert, Dumbbell, Sparkles } from "lucide-react";
import { useRouter } from "next/navigation";

import { ApiError, getCurrentUser, type CurrentUser, updateCurrentUser } from "@/lib/api";
import { hasCompletedFitnessSetup } from "@/lib/fitness-profile";

const goals = [
  ["weight_loss", "Lose weight"],
  ["weight_gain", "Gain weight"],
  ["muscle_gain", "Build muscle"],
  ["maintenance", "Maintain fitness"],
] as const;

const activityLevels = [
  ["sedentary", "Mostly seated"],
  ["light", "Lightly active"],
  ["moderate", "Moderately active"],
  ["active", "Active"],
  ["very_active", "Very active"],
] as const;

export default function OnboardingPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [age, setAge] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [sex, setSex] = useState("");
  const [goal, setGoal] = useState("muscle_gain");
  const [activity, setActivity] = useState("moderate");
  const [dietaryPreference, setDietaryPreference] = useState("balanced");
  const [workoutPreference, setWorkoutPreference] = useState("home");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadUser() {
      try {
        const profile = await getCurrentUser();
        if (cancelled) return;
        if (profile.is_admin) {
          router.replace("/admin");
          return;
        }
        if (hasCompletedFitnessSetup(profile)) {
          router.replace("/my-plan");
          return;
        }
        setUser(profile);
        setAge(profile.age ? String(profile.age) : "");
        setHeight(profile.height_cm ? String(profile.height_cm) : "");
        setWeight(profile.weight_kg ? String(profile.weight_kg) : "");
        setSex(profile.sex || "");
        setGoal(profile.fitness_goal || "muscle_gain");
        setActivity(profile.activity_level || "moderate");
        setDietaryPreference(profile.dietary_preference || "balanced");
        setWorkoutPreference(profile.workout_preference || "home");
      } catch (error) {
        if (!cancelled) {
          setErrorMessage(error instanceof ApiError ? error.detail : "Unable to load your account.");
          if (error instanceof ApiError && error.status === 401) router.replace("/login");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void loadUser();
    return () => { cancelled = true; };
  }, [router]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    const ageValue = Number(age);
    const heightValue = Number(height);
    const weightValue = Number(weight);
    if (!sex || !ageValue || !heightValue || !weightValue) {
      setErrorMessage("Choose the calorie-estimate option and enter age, height, and weight.");
      return;
    }
    setSaving(true);
    try {
      await updateCurrentUser({
        age: ageValue,
        height_cm: heightValue,
        weight_kg: weightValue,
        sex,
        fitness_goal: goal,
        dietary_preference: dietaryPreference,
        activity_level: activity,
        workout_preference: workoutPreference,
      });
      router.replace("/my-plan");
      router.refresh();
    } catch (error) {
      setErrorMessage(error instanceof ApiError ? error.detail : "We could not save your fitness setup.");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <main className="flex min-h-screen items-center justify-center bg-[#06070a] text-zinc-300">Preparing your fitness setup...</main>;
  }

  return (
    <main className="min-h-screen bg-[#06070a] px-5 py-8 text-white sm:py-12">
      <section className="mx-auto max-w-3xl rounded-[2rem] border border-white/10 bg-[#0a0c10] p-6 shadow-[0_35px_100px_rgba(0,0,0,0.45)] sm:p-9">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-cyan-400 text-black"><Sparkles size={23} /></div>
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-cyan-300">One-time fitness setup</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight">Let&apos;s build your plan{user ? `, ${user.full_name.split(" ")[0]}` : ""}.</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-zinc-400">Tell us your goal and workout setting once. AI Gym saves this to your profile, then uses it for your diet, daily workout, and AI Buddy guidance. You can edit it anytime.</p>
          </div>
        </div>

        {errorMessage && <div className="mt-6 flex gap-3 rounded-2xl border border-red-400/20 bg-red-400/5 p-4 text-sm text-red-200"><CircleAlert size={18} className="shrink-0" />{errorMessage}</div>}

        <form onSubmit={handleSubmit} className="mt-8 grid gap-5 sm:grid-cols-2">
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Age</span><input value={age} onChange={(event) => setAge(event.target.value)} type="number" min="13" max="120" required className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm outline-none focus:border-cyan-300/50" /></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Sex used for calorie estimates</span><select value={sex} onChange={(event) => setSex(event.target.value)} required className="h-12 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm outline-none focus:border-cyan-300/50"><option value="">Choose an option</option><option value="male">Male</option><option value="female">Female</option></select></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Height (cm)</span><input value={height} onChange={(event) => setHeight(event.target.value)} type="number" min="100" max="250" required className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm outline-none focus:border-cyan-300/50" /></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Weight (kg)</span><input value={weight} onChange={(event) => setWeight(event.target.value)} type="number" min="25" max="300" step="0.1" required className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] px-4 text-sm outline-none focus:border-cyan-300/50" /></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Primary goal</span><select value={goal} onChange={(event) => setGoal(event.target.value)} className="h-12 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm outline-none focus:border-cyan-300/50">{goals.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Activity level</span><select value={activity} onChange={(event) => setActivity(event.target.value)} className="h-12 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm outline-none focus:border-cyan-300/50">{activityLevels.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Food preference</span><select value={dietaryPreference} onChange={(event) => setDietaryPreference(event.target.value)} className="h-12 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm outline-none focus:border-cyan-300/50"><option value="balanced">Balanced</option><option value="vegetarian">Vegetarian</option><option value="vegan">Vegan</option><option value="high_protein">High protein</option><option value="low_carb">Lower carb</option></select></label>
          <label className="block"><span className="mb-2 block text-sm text-zinc-300">Where will you train?</span><select value={workoutPreference} onChange={(event) => setWorkoutPreference(event.target.value)} className="h-12 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm outline-none focus:border-cyan-300/50"><option value="home">At home</option><option value="gym">At a gym</option><option value="mixed">Home and gym</option></select></label>
          <div className="sm:col-span-2 mt-2 rounded-2xl border border-cyan-300/15 bg-cyan-300/[0.05] p-4 text-sm leading-6 text-zinc-300"><Dumbbell size={18} className="mr-2 inline text-cyan-300" />This creates a goal-based diet plan and a workout plan for your selected setting. Live AI Trainer currently provides real-time camera correction for squats.</div>
          <button type="submit" disabled={saving} className="sm:col-span-2 inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:opacity-50">{saving ? "Creating your plan..." : "Create my diet and workout plan"}<ArrowRight size={17} /></button>
        </form>
      </section>
    </main>
  );
}
