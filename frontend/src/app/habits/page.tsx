"use client";

import {
  Brain,
  CalendarClock,
  CircleAlert,
  HeartHandshake,
  RefreshCw,
  Target,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import {
  ApiError,
  getHabitAnalysis,
  type HabitAnalysis,
} from "@/lib/api";

function score(value: number): string {
  return `${Math.round(value)}%`;
}

function ScoreCard({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
      <div className="flex items-center justify-between gap-3">
        <p className="text-sm text-zinc-400">{label}</p>
        <p className="font-semibold text-cyan-300">{score(value)}</p>
      </div>
      <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/5">
        <div
          className="h-full rounded-full bg-cyan-400"
          style={{ width: `${Math.min(Math.max(value, 0), 100)}%` }}
        />
      </div>
    </div>
  );
}

export default function HabitsPage() {
  const router = useRouter();
  const [analysis, setAnalysis] = useState<HabitAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadAnalysis(showRefreshState = false) {
    if (showRefreshState) {
      setRefreshing(true);
    }

    setErrorMessage("");

    try {
      setAnalysis(await getHabitAnalysis());
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Habit analysis is not available right now.",
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialAnalysis() {
      try {
        const result = await getHabitAnalysis();
        if (!cancelled) {
          setAnalysis(result);
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
            : "Habit analysis is not available right now.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInitialAnalysis();

    return () => {
      cancelled = true;
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-6xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="Behavioral AI"
          title="Habit tracker"
          description="Turn your recent engagement signals into a clear workout recommendation and one useful next step."
          icon={Brain}
          action={
            <button
              type="button"
              onClick={() => void loadAnalysis(true)}
              disabled={loading || refreshing}
              className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-zinc-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCw
                size={16}
                className={refreshing ? "animate-spin" : ""}
              />
              {refreshing ? "Refreshing..." : "Refresh insight"}
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
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((item) => (
              <div
                key={item}
                className="h-32 animate-pulse rounded-2xl border border-white/10 bg-white/[0.025]"
              />
            ))}
          </div>
        ) : analysis ? (
          <>
            <section className="mt-8 grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
              <article className="rounded-3xl border border-cyan-300/15 bg-gradient-to-br from-cyan-400/[0.11] via-[#0d1117] to-[#0b0e13] p-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-cyan-300/15 bg-cyan-300/10 text-cyan-300">
                    <HeartHandshake size={20} />
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-[0.16em] text-cyan-200/70">
                      Your next best action
                    </p>
                    <h2 className="mt-2 text-xl font-semibold capitalize">
                      {analysis.nudge.action}
                    </h2>
                    <p className="mt-3 text-sm leading-6 text-zinc-300">
                      {analysis.nudge.message}
                    </p>
                  </div>
                </div>
                <div className="mt-6 inline-flex rounded-full border border-white/10 bg-white/5 px-3 py-1.5 text-xs capitalize text-zinc-300">
                  {analysis.nudge.urgency} priority
                </div>
              </article>

              <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
                <div className="flex items-center gap-3">
                  <CalendarClock size={19} className="text-cyan-300" />
                  <div>
                    <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                      Suggested session
                    </p>
                    <h2 className="mt-1 text-lg font-semibold capitalize">
                      {analysis.schedule.action}
                    </h2>
                  </div>
                </div>
                <div className="mt-5 grid grid-cols-2 gap-3">
                  <div className="rounded-2xl bg-white/[0.025] p-4">
                    <p className="text-xs text-zinc-600">Intensity</p>
                    <p className="mt-2 font-medium capitalize">
                      {analysis.schedule.intensity}
                    </p>
                  </div>
                  <div className="rounded-2xl bg-white/[0.025] p-4">
                    <p className="text-xs text-zinc-600">Duration</p>
                    <p className="mt-2 font-medium">
                      {analysis.schedule.duration_minutes} min
                    </p>
                  </div>
                </div>
                <p className="mt-4 text-sm leading-6 text-zinc-500">
                  {analysis.schedule.reason}
                </p>
              </article>
            </section>

            <section className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <ScoreCard
                label="Consistency"
                value={analysis.behavior.consistency_score}
              />
              <ScoreCard
                label="Motivation"
                value={analysis.behavior.motivation_score}
              />
              <ScoreCard
                label="Emotional stability"
                value={analysis.behavior.emotional_stability_score}
              />
              <ScoreCard
                label="Skip risk"
                value={analysis.skip_risk.probability}
              />
            </section>

            <section className="mt-5 grid gap-5 lg:grid-cols-2">
              <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-6">
                <div className="flex items-center gap-3">
                  <Target size={19} className="text-cyan-300" />
                  <div>
                    <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                      Attendance outlook
                    </p>
                    <h2 className="mt-1 text-lg font-semibold capitalize">
                      {analysis.skip_risk.level} risk
                    </h2>
                  </div>
                </div>
                <p className="mt-5 text-sm leading-6 text-zinc-400">
                  {analysis.skip_risk.reason}
                </p>
              </article>

              <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-6">
                <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Recent engagement signal
                </p>
                <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
                  <div className="rounded-xl bg-white/[0.025] p-4">
                    <p className="text-zinc-600">Sentiment</p>
                    <p className="mt-2 font-medium capitalize">
                      {analysis.memory.recent_sentiment}
                    </p>
                  </div>
                  <div className="rounded-xl bg-white/[0.025] p-4">
                    <p className="text-zinc-600">Motivation trend</p>
                    <p className="mt-2 font-medium capitalize">
                      {analysis.memory.motivation_trend}
                    </p>
                  </div>
                </div>
              </article>
            </section>
          </>
        ) : null}
      </div>
    </main>
  );
}
