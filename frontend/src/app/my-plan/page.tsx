"use client";

import { useEffect, useState } from "react";
import { Bot, CircleAlert, Dumbbell, Loader2, RefreshCw, Salad, Sparkles } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import { ApiError, getCurrentUser, type CurrentUser } from "@/lib/api";
import { hasCompletedFitnessSetup } from "@/lib/fitness-profile";
import { buildTodayPlan } from "@/lib/workout-plan";
import { generateDietPlan, type DietPlanResponse } from "@/lib/dieticianApi";

function number(value: number): string {
  return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 }).format(value);
}

export default function MyPlanPage() {
  const router = useRouter();
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [dietPlan, setDietPlan] = useState<DietPlanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function buildPlan(showRefreshing = false) {
    if (showRefreshing) setRefreshing(true);
    setErrorMessage("");
    try {
      const profile = await getCurrentUser();
      if (profile.is_admin) {
        router.replace("/admin");
        return;
      }
      if (!hasCompletedFitnessSetup(profile)) {
        router.replace("/onboarding");
        return;
      }
      const generatedDietPlan = await generateDietPlan();
      setUser(profile);
      setDietPlan(generatedDietPlan);
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }
      setErrorMessage(error instanceof ApiError ? error.detail : "Unable to build your personalized plan right now.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialPlan() {
      try {
        const profile = await getCurrentUser();

        if (cancelled) return;

        if (profile.is_admin) {
          router.replace("/admin");
          return;
        }

        if (!hasCompletedFitnessSetup(profile)) {
          router.replace("/onboarding");
          return;
        }

        const generatedDietPlan = await generateDietPlan();

        if (!cancelled) {
          setUser(profile);
          setDietPlan(generatedDietPlan);
        }
      } catch (error) {
        if (cancelled) return;

        if (error instanceof ApiError && error.status === 401) {
          router.replace("/login");
          return;
        }

        setErrorMessage(
          error instanceof ApiError
            ? error.detail
            : "Unable to build your personalized plan right now.",
        );
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void loadInitialPlan();

    return () => {
      cancelled = true;
    };
  }, [router]);

  const workoutPlan = buildTodayPlan(user);

  if (loading) {
    return <main className="flex min-h-screen items-center justify-center bg-[#06070a] text-zinc-300"><Loader2 className="mr-3 animate-spin" size={21} /> Building your fitness plan...</main>;
  }

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-7xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="Your saved fitness setup"
          title="My diet and workout plan"
          description="Built from your goal, body metrics, food preference, activity level, and training setting. Update these any time from your Profile."
          icon={Sparkles}
          action={<button type="button" onClick={() => void buildPlan(true)} disabled={refreshing} className="inline-flex h-11 items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-zinc-200 transition hover:bg-white/10 disabled:opacity-50"><RefreshCw size={16} className={refreshing ? "animate-spin" : ""} /> Refresh plan</button>}
        />

        {errorMessage && <div className="mt-6 flex gap-3 rounded-2xl border border-red-400/20 bg-red-400/5 p-4 text-sm leading-6 text-red-200"><CircleAlert size={18} className="mt-0.5 shrink-0" />{errorMessage}</div>}

        {!errorMessage && user && dietPlan && (
          <>
            <section className="mt-8 grid gap-4 md:grid-cols-4">
              {[ ["Goal", workoutPlan.goalLabel], ["Workout setting", workoutPlan.settingLabel], ["Daily calories", `${number(dietPlan.target_calories)} kcal`], ["Today", workoutPlan.duration] ].map(([label, value]) => <article key={label} className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5"><p className="text-xs uppercase tracking-[0.16em] text-zinc-600">{label}</p><p className="mt-3 text-lg font-semibold text-cyan-100">{value}</p></article>)}
            </section>

            <section className="mt-6 grid gap-6 xl:grid-cols-2">
              <article className="rounded-3xl border border-cyan-300/20 bg-gradient-to-br from-cyan-400/[0.12] to-[#0b0e13] p-6">
                <div className="flex items-start justify-between gap-4"><div><div className="flex items-center gap-3"><div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-200"><Dumbbell size={20} /></div><div><p className="text-xs uppercase tracking-[0.16em] text-cyan-200/70">Today&apos;s workout</p><h2 className="mt-1 text-xl font-semibold">{workoutPlan.focus}</h2></div></div><p className="mt-5 text-sm leading-6 text-zinc-300">Warm up first, then complete your main exercises with controlled form. Your plan is tailored for your {workoutPlan.settingLabel.toLowerCase()} setting.</p><p className="mt-3 rounded-xl border border-cyan-300/15 bg-cyan-300/[0.06] px-3 py-2 text-sm leading-6 text-cyan-50">{workoutPlan.goalNote}</p></div></div>
                <div className="mt-6 rounded-2xl border border-white/10 bg-black/15 p-4"><p className="text-xs font-medium uppercase tracking-[0.15em] text-zinc-500">Warm-up</p><ol className="mt-3 space-y-2 text-sm leading-6 text-zinc-300">{workoutPlan.warmup.map((item, index) => <li key={item} className="flex gap-3"><span className="font-semibold text-cyan-300">{index + 1}.</span>{item}</li>)}</ol></div>
                <div className="mt-4 space-y-3">{workoutPlan.workout.map((item, index) => <div key={item} className="flex gap-4 rounded-2xl border border-white/10 bg-white/[0.025] p-4"><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-400 text-xs font-bold text-black">{index + 1}</span><p className="text-sm leading-6 text-zinc-200">{item}</p></div>)}</div>
                <Link href="/live-trainer" className="mt-6 inline-flex h-11 items-center gap-2 rounded-xl bg-cyan-400 px-4 text-sm font-semibold text-black transition hover:bg-cyan-300"><Bot size={17} /> Start AI Buddy live coaching</Link>
              </article>

              <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
                <div className="flex items-center gap-3"><div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-emerald-300/15 bg-emerald-300/10 text-emerald-200"><Salad size={20} /></div><div><p className="text-xs uppercase tracking-[0.16em] text-zinc-600">Daily diet plan</p><h2 className="mt-1 text-xl font-semibold">{number(dietPlan.target_calories)} kcal target</h2></div></div>
                <div className="mt-6 space-y-3">{dietPlan.meals.map((meal) => <div key={meal.name} className="rounded-2xl border border-white/10 bg-white/[0.025] p-4"><div className="flex items-start justify-between gap-3"><div><h3 className="font-medium">{meal.name}</h3><p className="mt-1 text-xs text-zinc-500">{number(meal.protein_g)}g protein · {number(meal.carbohydrates_g)}g carbs · {number(meal.fat_g)}g fat</p></div><span className="text-sm font-semibold text-emerald-200">{number(meal.calories)} kcal</span></div></div>)}</div>
                <Link href="/dietician" className="mt-6 inline-flex h-11 items-center gap-2 rounded-xl border border-emerald-300/25 bg-emerald-300/10 px-4 text-sm font-semibold text-emerald-100 transition hover:bg-emerald-300/15"><Salad size={17} /> View plan and food log</Link>
              </article>
            </section>
          </>
        )}
      </div>
    </main>
  );
}
