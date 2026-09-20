"use client";

import {
  Activity,
  Bot,
  ChevronRight,
  Dumbbell,
  Gauge,
  HeartPulse,
  MapPin,
  MessageCircle,
  RefreshCw,
  Salad,
  ShieldCheck,
  Target,
  UserRound,
  Watch,
} from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import {
  ApiError,
  getAnalyticsSummary,
  getCurrentUser,
  logout,
  type CurrentUser,
  type FitnessAnalytics,
} from "@/lib/api";
import { hasCompletedFitnessSetup } from "@/lib/fitness-profile";

function formatNumber(
  value: number,
): string {
  return new Intl.NumberFormat(
    "en-IN",
  ).format(value);
}

function formatDecimal(
  value: number,
): string {
  return value.toFixed(1);
}

function StatCard({
  title,
  value,
  detail,
  icon: Icon,
}: {
  title: string;
  value: string;
  detail: string;
  icon: typeof Activity;
}) {
  return (
    <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5 transition hover:-translate-y-0.5 hover:border-cyan-300/15">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.15em] text-zinc-600">
            {title}
          </p>

          <p className="mt-3 text-3xl font-semibold tracking-tight">
            {value}
          </p>
        </div>

        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-300/10 bg-cyan-300/5 text-cyan-300">
          <Icon size={18} />
        </div>
      </div>

      <p className="mt-3 text-xs leading-5 text-zinc-600">
        {detail}
      </p>
    </article>
  );
}

function ModuleCard({
  title,
  description,
  href,
  icon: Icon,
}: {
  title: string;
  description: string;
  href: string;
  icon: typeof Activity;
}) {
  return (
    <Link
      href={href}
      className="group rounded-2xl border border-white/10 bg-[#0b0e13] p-5 transition hover:-translate-y-1 hover:border-cyan-300/20 hover:bg-[#0d1117]"
    >
      <div className="flex items-center justify-between">
        <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-cyan-300 transition group-hover:border-cyan-300/20 group-hover:bg-cyan-300/10">
          <Icon size={19} />
        </div>

        <ChevronRight
          size={17}
          className="text-zinc-700 transition group-hover:translate-x-1 group-hover:text-cyan-300"
        />
      </div>

      <h3 className="mt-5 text-sm font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-xs leading-5 text-zinc-600">
        {description}
      </p>
    </Link>
  );
}

export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] =
    useState<CurrentUser | null>(null);

  const [analytics, setAnalytics] =
    useState<FitnessAnalytics | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [refreshing, setRefreshing] =
    useState(false);

  const [errorMessage, setErrorMessage] =
    useState("");

  async function loadDashboard(
    showRefreshState = false,
  ) {
    if (showRefreshState) {
      setRefreshing(true);
    }

    setErrorMessage("");

    try {
      const [currentUser, analyticsData] =
        await Promise.all([
          getCurrentUser(),
          getAnalyticsSummary(),
        ]);

      if (!currentUser.is_admin && !hasCompletedFitnessSetup(currentUser)) {
        router.replace("/onboarding");
        return;
      }

      setUser(currentUser);
      setAnalytics(analyticsData);
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 401) {
          logout();
          router.replace("/login");
          return;
        }

        setErrorMessage(
          error.detail,
        );
      } else {
        setErrorMessage(
          "Unable to load your fitness dashboard.",
        );
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialDashboard() {
      try {
        const [currentUser, analyticsData] =
          await Promise.all([
            getCurrentUser(),
            getAnalyticsSummary(),
          ]);

        if (!currentUser.is_admin && !hasCompletedFitnessSetup(currentUser)) {
          router.replace("/onboarding");
          return;
        }

        if (!cancelled) {
          setUser(currentUser);
          setAnalytics(analyticsData);
          setLoading(false);
        }
      } catch (error) {
        if (cancelled) {
          return;
        }

        if (error instanceof ApiError) {
          if (error.status === 401) {
            logout();
            router.replace("/login");
            return;
          }

          setErrorMessage(
            error.detail,
          );
        } else {
          setErrorMessage(
            "Unable to load your fitness dashboard.",
          );
        }

        setLoading(false);
      }
    }

    void loadInitialDashboard();

    return () => {
      cancelled = true;
    };
  }, [router]);

  const firstName =
    user?.full_name.split(" ")[0] || "Athlete";

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <header className="border-b border-white/10 bg-[#090b0f]/90 px-5 py-4 backdrop-blur md:px-8">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs text-zinc-600">
                  AI Gym / Dashboard
                </p>

                <h1 className="mt-1 text-xl font-semibold md:text-2xl">
                  Welcome back, {firstName}.
                </h1>
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={() =>
                    void loadDashboard(true)
                  }
                  disabled={
                    loading || refreshing
                  }
                  className="hidden h-10 items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-xs font-medium text-zinc-300 transition hover:bg-white/10 disabled:opacity-50 sm:flex"
                >
                  <RefreshCw
                    size={15}
                    className={
                      refreshing
                        ? "animate-spin"
                        : ""
                    }
                  />

                  Refresh
                </button>

                <div className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-white/5 text-zinc-300">
                  <UserRound size={17} />
                </div>
              </div>
            </div>
      </header>

      <div className="mx-auto max-w-7xl px-5 py-7 md:px-8 md:py-9">
            {errorMessage && (
              <div className="mb-6 rounded-2xl border border-red-400/15 bg-red-400/5 px-4 py-3 text-sm text-red-300">
                {errorMessage}
              </div>
            )}

            {loading ? (
              <div className="space-y-6">
                <div className="h-52 animate-pulse rounded-3xl border border-white/10 bg-white/[0.025]" />

                <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                  {[1, 2, 3, 4].map(
                    (item) => (
                      <div
                        key={item}
                        className="h-36 animate-pulse rounded-2xl border border-white/10 bg-white/[0.025]"
                      />
                    ),
                  )}
                </div>
              </div>
            ) : analytics ? (
              <>
                <section className="relative overflow-hidden rounded-3xl border border-cyan-300/10 bg-gradient-to-br from-cyan-400/[0.11] via-[#0d1118] to-[#0b0d12] p-6 md:p-8">
                  <div className="pointer-events-none absolute -right-24 -top-24 h-64 w-64 rounded-full bg-cyan-300/10 blur-3xl" />

                  <div className="relative max-w-3xl">
                    <div className="inline-flex items-center gap-2 rounded-full border border-cyan-300/15 bg-cyan-300/5 px-3 py-1.5 text-xs font-medium text-cyan-200">
                      <Bot size={14} />
                      AI fitness intelligence
                    </div>

                    <h2 className="mt-5 text-3xl font-semibold tracking-tight md:text-5xl">
                      Your fitness system is
                      <span className="text-cyan-300">
                        {" "}
                        connected.
                      </span>
                    </h2>

                    <p className="mt-4 max-w-2xl text-sm leading-7 text-zinc-500 md:text-base">
                      Your workout, nutrition, and Smart Gym
                      signals are now available through one
                      adaptive dashboard.
                    </p>
                  </div>
                </section>

                <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                  <StatCard
                    title="Workouts"
                    value={formatNumber(
                      analytics.workouts
                        .total_workouts,
                    )}
                    detail={`${formatNumber(analytics.workouts.total_repetitions)} tracked repetitions`}
                    icon={Dumbbell}
                  />

                  <StatCard
                    title="Performance"
                    value={`${formatDecimal(analytics.workouts.average_performance_score)}%`}
                    detail={`Best session: ${formatDecimal(analytics.workouts.best_performance_score)}%`}
                    icon={Gauge}
                  />

                  <StatCard
                    title="Nutrition"
                    value={formatNumber(
                      Math.round(
                        analytics.nutrition
                          .total_calories,
                      ),
                    )}
                    detail={`${formatNumber(analytics.nutrition.total_food_entries)} food entries logged`}
                    icon={Salad}
                  />

                  <StatCard
                    title="Recovery Signal"
                    value={`${formatDecimal(100 - analytics.smart_gym.average_fatigue_level)}%`}
                    detail={`Average fatigue: ${formatDecimal(analytics.smart_gym.average_fatigue_level)}%`}
                    icon={HeartPulse}
                  />
                </section>

                <section className="mt-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
                  <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                          Nutrition intelligence
                        </p>

                        <h2 className="mt-2 text-xl font-semibold">
                          Nutrition overview
                        </h2>
                      </div>

                      <Salad
                        size={20}
                        className="text-cyan-300"
                      />
                    </div>

                    <div className="mt-6 grid gap-3 sm:grid-cols-2">
                      {[
                        [
                          "Calories",
                          `${formatNumber(Math.round(analytics.nutrition.total_calories))} kcal`,
                        ],
                        [
                          "Protein",
                          `${formatDecimal(analytics.nutrition.total_protein_g)} g`,
                        ],
                        [
                          "Carbohydrates",
                          `${formatDecimal(analytics.nutrition.total_carbohydrates_g)} g`,
                        ],
                        [
                          "Fat",
                          `${formatDecimal(analytics.nutrition.total_fat_g)} g`,
                        ],
                      ].map(
                        ([label, value]) => (
                          <div
                            key={label}
                            className="rounded-2xl border border-white/5 bg-white/[0.025] p-4"
                          >
                            <p className="text-xs text-zinc-600">
                              {label}
                            </p>

                            <p className="mt-2 text-lg font-semibold">
                              {value}
                            </p>
                          </div>
                        ),
                      )}
                    </div>
                  </article>

                  <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                          Smart Gym
                        </p>

                        <h2 className="mt-2 text-xl font-semibold">
                          Live intelligence
                        </h2>
                      </div>

                      <Watch
                        size={20}
                        className="text-cyan-300"
                      />
                    </div>

                    <div className="mt-6 space-y-1">
                      <div className="flex items-center justify-between border-b border-white/5 py-3">
                        <span className="text-sm text-zinc-500">
                          Equipment
                        </span>

                        <span className="font-medium">
                          {formatNumber(
                            analytics.smart_gym
                              .equipment_count,
                          )}
                        </span>
                      </div>

                      <div className="flex items-center justify-between border-b border-white/5 py-3">
                        <span className="text-sm text-zinc-500">
                          Avg. heart rate
                        </span>

                        <span className="font-medium">
                          {formatDecimal(
                            analytics.smart_gym
                              .average_heart_rate,
                          )}{" "}
                          bpm
                        </span>
                      </div>

                      <div className="flex items-center justify-between border-b border-white/5 py-3">
                        <span className="text-sm text-zinc-500">
                          Avg. resistance
                        </span>

                        <span className="font-medium">
                          {formatDecimal(
                            analytics.smart_gym
                              .average_resistance,
                          )}
                        </span>
                      </div>

                      <div className="flex items-center justify-between py-3">
                        <span className="text-sm text-zinc-500">
                          AI commands
                        </span>

                        <span className="font-medium">
                          {formatNumber(
                            analytics.smart_gym
                              .total_commands,
                          )}
                        </span>
                      </div>
                    </div>
                  </article>
                </section>

                <section className="mt-6">
                  <div className="flex items-end justify-between gap-4">
                    <div>
                      <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                        AI ecosystem
                      </p>

                      <h2 className="mt-2 text-xl font-semibold">
                        Open a fitness module
                      </h2>
                    </div>

                    <span className="hidden text-xs text-zinc-700 sm:block">
                      Adaptive workspace
                    </span>
                  </div>

                  <div className="mt-5 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                    <ModuleCard
                      title="AI Trainer"
                      description="Analyze recorded workout sessions and review performance."
                      href="/trainer"
                      icon={Dumbbell}
                    />

                    <ModuleCard
                      title="Dietician"
                      description="Generate personalized nutrition targets, meals, and grocery lists."
                      href="/dietician"
                      icon={Salad}
                    />

                    <ModuleCard
                      title="Gym Buddy"
                      description="Chat with your fitness companion and review motivation signals."
                      href="/gym-buddy"
                      icon={MessageCircle}
                    />

                    <ModuleCard
                      title="Habit AI"
                      description="Review consistency, behavioral risk, nudges, and schedule adaptations."
                      href="/habits"
                      icon={Target}
                    />

                    <ModuleCard
                      title="Pose Analysis"
                      description="Review posture and pose-based performance analysis."
                      href="/pose-analysis"
                      icon={Activity}
                    />

                    <ModuleCard
                      title="Smart Gym"
                      description="Inspect equipment intelligence, telemetry, and AI commands."
                      href="/smart-gym"
                      icon={Watch}
                    />

                    <ModuleCard
                      title="Fitness Planner"
                      description="Generate gym, program, and challenge recommendations for your goal."
                      href="/planner"
                      icon={MapPin}
                    />

                    <ModuleCard
                      title="Analytics"
                      description="Explore the unified fitness analytics generated from your activity."
                      href="/analytics"
                      icon={HeartPulse}
                    />

                    <ModuleCard
                      title="Profile"
                      description="View and manage your fitness profile and account information."
                      href="/profile"
                      icon={UserRound}
                    />
                  </div>
                </section>

                <section className="mt-8 rounded-2xl border border-white/10 bg-[#0b0e13] p-5">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-emerald-400/10 bg-emerald-400/5 text-emerald-300">
                      <ShieldCheck size={18} />
                    </div>

                    <div>
                      <p className="text-sm font-medium">
                        Workspace authenticated
                      </p>

                      <p className="mt-1 text-xs text-zinc-600">
                        {user?.email}
                      </p>
                    </div>

                    <div className="ml-auto flex items-center gap-2 text-xs text-emerald-300">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-300" />
                      Active
                    </div>
                  </div>
                </section>
              </>
            ) : null}
      </div>
    </main>
  );
}
