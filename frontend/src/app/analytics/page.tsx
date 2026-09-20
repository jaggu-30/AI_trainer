"use client";

import {
  Activity,
  BarChart3,
  CircleAlert,
  Dumbbell,
  RefreshCw,
  Salad,
  TrendingUp,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import {
  ApiError,
  getAnalyticsSummary,
  getWeeklyPerformance,
  type FitnessAnalytics,
  type WeeklyPerformance,
} from "@/lib/api";

function number(value: number): string {
  return new Intl.NumberFormat("en-IN").format(Math.round(value));
}

function percent(value: number): string {
  return `${value.toFixed(1)}%`;
}

function ProgressRow({ label, value }: { label: string; value: number }) {
  const clamped = Math.min(Math.max(value, 0), 100);

  return (
    <div>
      <div className="flex items-center justify-between gap-4 text-sm">
        <span className="text-zinc-400">{label}</span>
        <span className="font-medium text-cyan-300">{percent(value)}</span>
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-white/5">
        <div
          className="h-full rounded-full bg-gradient-to-r from-cyan-400 to-emerald-300"
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
}

export default function AnalyticsPage() {
  const router = useRouter();
  const [summary, setSummary] = useState<FitnessAnalytics | null>(null);
  const [weekly, setWeekly] = useState<WeeklyPerformance | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadAnalytics(showRefreshState = false) {
    if (showRefreshState) {
      setRefreshing(true);
    }

    setErrorMessage("");

    try {
      const [analytics, performance] = await Promise.all([
        getAnalyticsSummary(),
        getWeeklyPerformance(),
      ]);
      setSummary(analytics);
      setWeekly(performance);
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Analytics are not available right now.",
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialAnalytics() {
      try {
        const [analytics, performance] = await Promise.all([
          getAnalyticsSummary(),
          getWeeklyPerformance(),
        ]);
        if (!cancelled) {
          setSummary(analytics);
          setWeekly(performance);
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
            : "Analytics are not available right now.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInitialAnalytics();

    return () => {
      cancelled = true;
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-6xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="Fitness intelligence"
          title="Analytics"
          description="A simple, unified view of your workout, nutrition, recovery, and weekly performance signals."
          icon={BarChart3}
          action={
            <button
              type="button"
              onClick={() => void loadAnalytics(true)}
              disabled={loading || refreshing}
              className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-zinc-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCw
                size={16}
                className={refreshing ? "animate-spin" : ""}
              />
              {refreshing ? "Refreshing..." : "Refresh data"}
            </button>
          }
        />

        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/5 p-4 text-sm text-red-300">
            <CircleAlert size={18} className="mt-0.5 shrink-0" />
            <p>{errorMessage}</p>
          </div>
        )}

        {loading ? (
          <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {[1, 2, 3, 4].map((item) => (
              <div
                key={item}
                className="h-32 animate-pulse rounded-2xl border border-white/10 bg-white/[0.025]"
              />
            ))}
          </div>
        ) : summary && weekly ? (
          <>
            <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {[
                ["Workouts", number(summary.workouts.total_workouts), Dumbbell],
                ["Performance", percent(summary.workouts.average_performance_score), TrendingUp],
                ["Food entries", number(summary.nutrition.total_food_entries), Salad],
                ["Recovery", percent(100 - summary.smart_gym.average_fatigue_level), Activity],
              ].map(([label, value, Icon]) => {
                const MetricIcon = Icon as typeof Activity;
                return (
                  <article
                    key={label as string}
                    className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5"
                  >
                    <MetricIcon size={19} className="text-cyan-300" />
                    <p className="mt-4 text-xs uppercase tracking-[0.16em] text-zinc-600">
                      {label as string}
                    </p>
                    <p className="mt-2 text-2xl font-semibold">{value as string}</p>
                  </article>
                );
              })}
            </section>

            <section className="mt-5 grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
              <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
                <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                  This week
                </p>
                <div className="mt-4 flex flex-wrap items-end justify-between gap-4">
                  <div>
                    <h2 className="text-3xl font-semibold">
                      {percent(weekly.average_performance_score)}
                    </h2>
                    <p className="mt-1 text-sm text-zinc-500">
                      Average performance across {weekly.workout_count} sessions
                    </p>
                  </div>
                  <span className="rounded-full border border-cyan-300/15 bg-cyan-300/5 px-3 py-1.5 text-xs capitalize text-cyan-200">
                    {weekly.performance_trend} trend
                  </span>
                </div>
                <p className="mt-5 rounded-2xl bg-white/[0.025] p-4 text-sm leading-6 text-zinc-400">
                  {weekly.summary}
                </p>
              </article>

              <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
                <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Nutrition totals
                </p>
                <div className="mt-5 space-y-4 text-sm">
                  <div className="flex justify-between gap-4">
                    <span className="text-zinc-500">Calories</span>
                    <span className="font-medium">{number(summary.nutrition.total_calories)} kcal</span>
                  </div>
                  <div className="flex justify-between gap-4">
                    <span className="text-zinc-500">Protein</span>
                    <span className="font-medium">{summary.nutrition.total_protein_g.toFixed(1)} g</span>
                  </div>
                  <div className="flex justify-between gap-4">
                    <span className="text-zinc-500">Carbohydrates</span>
                    <span className="font-medium">{summary.nutrition.total_carbohydrates_g.toFixed(1)} g</span>
                  </div>
                  <div className="flex justify-between gap-4">
                    <span className="text-zinc-500">Fat</span>
                    <span className="font-medium">{summary.nutrition.total_fat_g.toFixed(1)} g</span>
                  </div>
                </div>
              </article>
            </section>

            <section className="mt-5 rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
              <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                Movement quality
              </p>
              <h2 className="mt-2 text-xl font-semibold">Weekly form scores</h2>
              <div className="mt-6 grid gap-5 md:grid-cols-3">
                <ProgressRow label="Depth" value={weekly.average_depth_score} />
                <ProgressRow label="Posture" value={weekly.average_posture_score} />
                <ProgressRow label="Control" value={weekly.average_control_score} />
              </div>
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
