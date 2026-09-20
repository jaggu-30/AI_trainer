"use client";

import {
  Activity,
  CircleAlert,
  Clock3,
  RefreshCw,
  Sparkles,
  Upload,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import {
  ApiError,
  getWeeklyPerformance,
  getWorkoutHistory,
  type WeeklyPerformance,
  type WorkoutHistory,
} from "@/lib/api";

function dateLabel(value: string): string {
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : date.toLocaleDateString("en-IN", {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
}

function score(value: number): string {
  return `${value.toFixed(1)}%`;
}

export default function PoseAnalysisPage() {
  const router = useRouter();
  const [history, setHistory] = useState<WorkoutHistory | null>(null);
  const [weekly, setWeekly] = useState<WeeklyPerformance | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadPerformance(showRefreshState = false) {
    if (showRefreshState) {
      setRefreshing(true);
    }

    setErrorMessage("");

    try {
      const [workouts, performance] = await Promise.all([
        getWorkoutHistory(6),
        getWeeklyPerformance(),
      ]);
      setHistory(workouts);
      setWeekly(performance);
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Performance analysis is not available right now.",
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialPerformance() {
      try {
        const [workouts, performance] = await Promise.all([
          getWorkoutHistory(6),
          getWeeklyPerformance(),
        ]);
        if (!cancelled) {
          setHistory(workouts);
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
            : "Performance analysis is not available right now.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInitialPerformance();

    return () => {
      cancelled = true;
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-6xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="Motion intelligence"
          title="Pose-to-performance"
          description="Use the AI Trainer to analyze a recording, then review the form-quality scores and weekly progression here."
          icon={Activity}
          action={
            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => void loadPerformance(true)}
                disabled={loading || refreshing}
                className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-zinc-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
              >
                <RefreshCw
                  size={16}
                  className={refreshing ? "animate-spin" : ""}
                />
                Refresh
              </button>
              <Link
                href="/trainer"
                className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-cyan-400 px-4 text-sm font-semibold text-black transition hover:bg-cyan-300"
              >
                <Upload size={16} />
                Analyze a video
              </Link>
            </div>
          }
        />

        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/5 p-4 text-sm text-red-300">
            <CircleAlert size={18} className="mt-0.5 shrink-0" />
            <p>{errorMessage}</p>
          </div>
        )}

        {loading ? (
          <div className="mt-8 h-80 animate-pulse rounded-3xl border border-white/10 bg-white/[0.025]" />
        ) : history && weekly ? (
          <>
            <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {[
                ["Average score", score(weekly.average_performance_score)],
                ["Best score", score(weekly.best_performance_score)],
                ["Sessions", String(weekly.workout_count)],
                ["Repetitions", String(weekly.total_repetitions)],
              ].map(([label, value]) => (
                <article
                  key={label}
                  className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5"
                >
                  <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                    {label}
                  </p>
                  <p className="mt-3 text-2xl font-semibold text-cyan-300">
                    {value}
                  </p>
                </article>
              ))}
            </section>

            <section className="mt-5 grid gap-5 lg:grid-cols-[0.92fr_1.08fr]">
              <article className="rounded-3xl border border-cyan-300/15 bg-gradient-to-br from-cyan-400/[0.1] to-[#0b0e13] p-6">
                <Sparkles size={20} className="text-cyan-300" />
                <p className="mt-5 text-xs uppercase tracking-[0.16em] text-cyan-200/70">
                  Weekly coach note
                </p>
                <h2 className="mt-2 text-xl font-semibold capitalize">
                  {weekly.performance_trend} momentum
                </h2>
                <p className="mt-4 text-sm leading-6 text-zinc-300">
                  {weekly.summary}
                </p>
                <div className="mt-6 grid grid-cols-3 gap-3 text-center text-sm">
                  {[
                    ["Depth", weekly.average_depth_score],
                    ["Posture", weekly.average_posture_score],
                    ["Control", weekly.average_control_score],
                  ].map(([label, value]) => (
                    <div key={label as string} className="rounded-xl bg-black/15 p-3">
                      <p className="text-xs text-zinc-500">{label as string}</p>
                      <p className="mt-1 font-semibold text-cyan-200">
                        {score(value as number)}
                      </p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
                <div className="flex items-center gap-3">
                  <Clock3 size={19} className="text-cyan-300" />
                  <div>
                    <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                      Recent analyses
                    </p>
                    <h2 className="mt-1 text-lg font-semibold">Workout history</h2>
                  </div>
                </div>

                {history.items.length === 0 ? (
                  <p className="mt-8 rounded-2xl bg-white/[0.025] p-5 text-sm leading-6 text-zinc-500">
                    No completed workout analyses yet. Upload a recording to create your first performance report.
                  </p>
                ) : (
                  <div className="mt-5 divide-y divide-white/5">
                    {history.items.map((workout) => (
                      <div
                        key={workout.id}
                        className="flex items-center justify-between gap-4 py-4"
                      >
                        <div>
                          <p className="font-medium capitalize">
                            {workout.exercise.replace(/_/g, " ")}
                          </p>
                          <p className="mt-1 text-xs text-zinc-600">
                            {dateLabel(workout.completed_at)} · {workout.total_repetitions} reps
                          </p>
                        </div>
                        <span className="text-sm font-semibold text-cyan-300">
                          {score(workout.performance_score)}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </article>
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
