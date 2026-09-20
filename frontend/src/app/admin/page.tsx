"use client";

import {
  Activity,
  ArrowLeft,
  Bot,
  CircleAlert,
  Database,
  Dumbbell,
  Gauge,
  MessageCircle,
  RefreshCw,
  Salad,
  ShieldCheck,
  Users,
  Watch,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import {
  ApiError,
  getAdminUsers,
  getAdminSummary,
  getCurrentUser,
  logout,
  updateAdminUserStatus,
  type AdminSummary,
  type AdminUser,
  type CurrentUser,
} from "@/lib/api";

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

function formatDate(
  value: string,
): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleDateString(
    "en-IN",
    {
      day: "numeric",
      month: "short",
      year: "numeric",
    },
  );
}

function StatCard({
  title,
  value,
  description,
  icon: Icon,
}: {
  title: string;
  value: string;
  description: string;
  icon: typeof Users;
}) {
  return (
    <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5 transition hover:-translate-y-0.5 hover:border-cyan-300/15">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
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
        {description}
      </p>
    </article>
  );
}

function SectionCard({
  title,
  icon: Icon,
  children,
}: {
  title: string;
  icon: typeof Users;
  children: React.ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-white/10 bg-[#0b0e13] p-6">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/5 text-cyan-300">
          <Icon size={18} />
        </div>

        <h2 className="text-lg font-semibold">
          {title}
        </h2>
      </div>

      <div className="mt-6">
        {children}
      </div>
    </section>
  );
}

function MetricRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between gap-5 border-b border-white/5 py-3 last:border-0">
      <span className="text-sm text-zinc-500">
        {label}
      </span>

      <span className="text-sm font-medium text-white">
        {value}
      </span>
    </div>
  );
}

export default function AdminPage() {
  const router = useRouter();
  const [summary, setSummary] =
    useState<AdminSummary | null>(null);

  const [users, setUsers] =
    useState<AdminUser[]>([]);

  const [totalUsers, setTotalUsers] =
    useState(0);

  const [administrator, setAdministrator] =
    useState<CurrentUser | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [refreshing, setRefreshing] =
    useState(false);

  const [errorMessage, setErrorMessage] =
    useState("");

  const [updatingUserId, setUpdatingUserId] =
    useState<number | null>(null);

  const [loadingMoreUsers, setLoadingMoreUsers] =
    useState(false);

  async function loadSummary(
    showRefreshState = false,
  ) {
    if (showRefreshState) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    setErrorMessage("");

    try {
      const [result, directory] =
        await Promise.all([
          getAdminSummary(),
          getAdminUsers(),
        ]);

      setSummary(result);
      setUsers(directory.items);
      setTotalUsers(directory.total);
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 401 || error.status === 403) {
          logout();
          router.replace("/admin/login");
          return;
        } else {
          setErrorMessage(
            error.detail,
          );
        }
      } else {
        setErrorMessage(
          "Unable to load the admin dashboard.",
        );
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  async function handleUserStatus(
    user: AdminUser,
  ) {
    setUpdatingUserId(user.id);
    setErrorMessage("");

    try {
      const updated = await updateAdminUserStatus(
        user.id,
        !user.is_active,
      );

      setUsers((currentUsers) =>
        currentUsers.map((item) =>
          item.id === updated.id ? updated : item,
        ),
      );

      setSummary(await getAdminSummary());
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 401 || error.status === 403) {
          logout();
          router.replace("/admin/login");
          return;
        }

        setErrorMessage(error.detail);
      } else {
        setErrorMessage("Unable to update this user account.");
      }
    } finally {
      setUpdatingUserId(null);
    }
  }

  async function loadMoreUsers() {
    setLoadingMoreUsers(true);
    setErrorMessage("");

    try {
      const directory = await getAdminUsers(
        100,
        users.length,
      );

      setUsers((currentUsers) => [
        ...currentUsers,
        ...directory.items,
      ]);
      setTotalUsers(directory.total);
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 401 || error.status === 403) {
          logout();
          router.replace("/admin/login");
          return;
        }

        setErrorMessage(error.detail);
      } else {
        setErrorMessage("Unable to load more users.");
      }
    } finally {
      setLoadingMoreUsers(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialSummary() {
      setErrorMessage("");

      try {
        const account = await getCurrentUser();

        if (!account.is_admin) {
          logout();
          router.replace("/admin/login");
          return;
        }

        const [result, directory] =
          await Promise.all([
            getAdminSummary(),
            getAdminUsers(),
          ]);

        if (!cancelled) {
          setAdministrator(account);
          setSummary(result);
          setUsers(directory.items);
          setTotalUsers(directory.total);
        }
      } catch (error) {
        if (cancelled) {
          return;
        }

        if (error instanceof ApiError) {
          if (error.status === 401 || error.status === 403) {
            logout();
            router.replace("/admin/login");
            return;
          } else {
            setErrorMessage(
              error.detail,
            );
          }
        } else {
          setErrorMessage(
            "Unable to load the admin dashboard.",
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInitialSummary();

    return () => {
      cancelled = true;
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-7xl px-5 py-7 md:px-8 md:py-10">
        <header className="flex flex-col gap-5 border-b border-white/10 pb-7 md:flex-row md:items-end md:justify-between">
          <div>
            <Link
              href="/"
              className="inline-flex items-center gap-2 text-xs text-zinc-600 transition hover:text-cyan-300"
            >
              <ArrowLeft size={14} />
              Back to dashboard
            </Link>

            <div className="mt-5 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-400 text-black shadow-[0_0_35px_rgba(34,211,238,0.3)]">
                <ShieldCheck size={22} />
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-cyan-300">
                  AI Gym
                </p>

                <h1 className="mt-1 text-2xl font-semibold tracking-tight md:text-3xl">
                  Admin Dashboard
                </h1>
              </div>
            </div>

            <p className="mt-4 max-w-2xl text-sm leading-6 text-zinc-500">
              System-wide visibility across users, workouts,
              nutrition, conversations, and Smart Gym telemetry.
            </p>
          </div>

          <button
            type="button"
            onClick={() =>
              void loadSummary(true)
            }
            disabled={
              loading || refreshing
            }
            className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-white transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <RefreshCw
              size={16}
              className={
                refreshing
                  ? "animate-spin"
                  : ""
              }
            />

            {refreshing
              ? "Refreshing..."
              : "Refresh data"}
          </button>
        </header>

        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/5 p-4 text-sm leading-6 text-red-300">
            <CircleAlert
              size={18}
              className="mt-0.5 shrink-0"
            />

            <div>
              <p className="font-medium">
                Unable to load dashboard
              </p>

              <p className="mt-1 text-red-300/80">
                {errorMessage}
              </p>
            </div>
          </div>
        )}

        {loading ? (
          <div className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {[1, 2, 3, 4].map(
              (item) => (
                <div
                  key={item}
                  className="h-36 animate-pulse rounded-2xl border border-white/10 bg-white/[0.025]"
                />
              ),
            )}
          </div>
        ) : summary ? (
          <>
            <section className="mt-8 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <StatCard
                title="Total Users"
                value={formatNumber(
                  summary.users.total_users,
                )}
                description={`${formatNumber(summary.users.active_users)} active users`}
                icon={Users}
              />

              <StatCard
                title="Total Workouts"
                value={formatNumber(
                  summary.workouts.total_workouts,
                )}
                description={`${formatNumber(summary.workouts.total_repetitions)} tracked repetitions`}
                icon={Dumbbell}
              />

              <StatCard
                title="Food Entries"
                value={formatNumber(
                  summary.nutrition.total_food_entries,
                )}
                description={`${formatNumber(Math.round(summary.nutrition.total_calories))} total calories logged`}
                icon={Salad}
              />

              <StatCard
                title="Chat Messages"
                value={formatNumber(
                  summary.chat.total_messages,
                )}
                description={`${formatNumber(summary.chat.total_sessions)} conversation sessions`}
                icon={MessageCircle}
              />
            </section>

            <section className="mt-6 grid gap-6 lg:grid-cols-2">
              <SectionCard
                title="Users"
                icon={Users}
              >
                <MetricRow
                  label="Total users"
                  value={formatNumber(
                    summary.users.total_users,
                  )}
                />

                <MetricRow
                  label="Active users"
                  value={formatNumber(
                    summary.users.active_users,
                  )}
                />

                <MetricRow
                  label="Inactive users"
                  value={formatNumber(
                    summary.users.inactive_users,
                  )}
                />

                <MetricRow
                  label="Administrators"
                  value={formatNumber(
                    summary.users.admin_users,
                  )}
                />
              </SectionCard>

              <SectionCard
                title="Workout Intelligence"
                icon={Dumbbell}
              >
                <MetricRow
                  label="Total workouts"
                  value={formatNumber(
                    summary.workouts.total_workouts,
                  )}
                />

                <MetricRow
                  label="Total repetitions"
                  value={formatNumber(
                    summary.workouts.total_repetitions,
                  )}
                />

                <MetricRow
                  label="Average performance"
                  value={`${formatDecimal(summary.workouts.average_performance_score)}%`}
                />

                <MetricRow
                  label="Best performance"
                  value={`${formatDecimal(summary.workouts.best_performance_score)}%`}
                />
              </SectionCard>

              <SectionCard
                title="Nutrition"
                icon={Salad}
              >
                <MetricRow
                  label="Food entries"
                  value={formatNumber(
                    summary.nutrition.total_food_entries,
                  )}
                />

                <MetricRow
                  label="Calories"
                  value={`${formatNumber(Math.round(summary.nutrition.total_calories))} kcal`}
                />

                <MetricRow
                  label="Protein"
                  value={`${formatDecimal(summary.nutrition.total_protein_g)} g`}
                />

                <MetricRow
                  label="Carbohydrates"
                  value={`${formatDecimal(summary.nutrition.total_carbohydrates_g)} g`}
                />

                <MetricRow
                  label="Fat"
                  value={`${formatDecimal(summary.nutrition.total_fat_g)} g`}
                />
              </SectionCard>

              <SectionCard
                title="Conversation Intelligence"
                icon={MessageCircle}
              >
                <MetricRow
                  label="Chat sessions"
                  value={formatNumber(
                    summary.chat.total_sessions,
                  )}
                />

                <MetricRow
                  label="Total messages"
                  value={formatNumber(
                    summary.chat.total_messages,
                  )}
                />

                <MetricRow
                  label="User messages"
                  value={formatNumber(
                    summary.chat.user_messages,
                  )}
                />

                <MetricRow
                  label="AI responses"
                  value={formatNumber(
                    summary.chat.assistant_messages,
                  )}
                />
              </SectionCard>
            </section>

            <section className="mt-6 rounded-2xl border border-white/10 bg-[#0b0e13] p-6">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                    Account administration
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">
                    User directory
                  </h2>
                  <p className="mt-2 text-sm text-zinc-500">
                    {formatNumber(totalUsers)} registered users. Activate or deactivate user access as needed.
                  </p>
                </div>

                <span className="rounded-full border border-cyan-300/15 bg-cyan-300/5 px-3 py-1.5 text-xs text-cyan-200">
                  Admin-only controls
                </span>
              </div>

              <div className="mt-6 overflow-x-auto rounded-xl border border-white/5">
                <table className="min-w-[720px] w-full text-left text-sm">
                  <thead className="bg-white/[0.025] text-xs uppercase tracking-[0.12em] text-zinc-600">
                    <tr>
                      <th className="px-4 py-3 font-medium">User</th>
                      <th className="px-4 py-3 font-medium">Role</th>
                      <th className="px-4 py-3 font-medium">Joined</th>
                      <th className="px-4 py-3 font-medium">Status</th>
                      <th className="px-4 py-3 text-right font-medium">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-white/5">
                    {users.map((user) => {
                      const isCurrentAdmin = user.id === administrator?.id;
                      const isUpdating = updatingUserId === user.id;

                      return (
                        <tr key={user.id} className="text-zinc-300">
                          <td className="px-4 py-4">
                            <p className="font-medium text-white">{user.full_name}</p>
                            <p className="mt-1 text-xs text-zinc-600">{user.email}</p>
                          </td>
                          <td className="px-4 py-4">
                            <span className={`rounded-full px-2.5 py-1 text-xs ${
                              user.is_admin
                                ? "bg-cyan-300/10 text-cyan-200"
                                : "bg-white/5 text-zinc-400"
                            }`}>
                              {user.is_admin ? "Administrator" : "User"}
                            </span>
                          </td>
                          <td className="px-4 py-4 text-zinc-500">
                            {formatDate(user.created_at)}
                          </td>
                          <td className="px-4 py-4">
                            <span className={`inline-flex items-center gap-2 text-xs ${
                              user.is_active ? "text-emerald-300" : "text-amber-300"
                            }`}>
                              <span className={`h-1.5 w-1.5 rounded-full ${
                                user.is_active ? "bg-emerald-300" : "bg-amber-300"
                              }`} />
                              {user.is_active ? "Active" : "Inactive"}
                            </span>
                          </td>
                          <td className="px-4 py-4 text-right">
                            <button
                              type="button"
                              onClick={() => void handleUserStatus(user)}
                              disabled={isUpdating || isCurrentAdmin}
                              title={isCurrentAdmin ? "You cannot deactivate your own account." : undefined}
                              className={`rounded-lg border px-3 py-2 text-xs font-medium transition disabled:cursor-not-allowed disabled:opacity-40 ${
                                user.is_active
                                  ? "border-red-400/20 text-red-300 hover:bg-red-400/10"
                                  : "border-emerald-400/20 text-emerald-300 hover:bg-emerald-400/10"
                              }`}
                            >
                              {isUpdating
                                ? "Updating..."
                                : user.is_active
                                  ? "Deactivate"
                                  : "Activate"}
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              {users.length < totalUsers && (
                <div className="mt-5 flex justify-center">
                  <button
                    type="button"
                    onClick={() => void loadMoreUsers()}
                    disabled={loadingMoreUsers}
                    className="rounded-xl border border-white/10 bg-white/[0.025] px-4 py-2.5 text-sm font-medium text-zinc-300 transition hover:border-cyan-300/30 hover:text-cyan-200 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {loadingMoreUsers ? "Loading users..." : "Load more users"}
                  </button>
                </div>
              )}
            </section>

            <section className="mt-6 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
              <SectionCard
                title="Smart Gym Operations"
                icon={Watch}
              >
                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <div className="flex items-center gap-3">
                      <Gauge
                        size={18}
                        className="text-cyan-300"
                      />

                      <p className="text-sm text-zinc-500">
                        Equipment
                      </p>
                    </div>

                    <p className="mt-3 text-2xl font-semibold">
                      {formatNumber(
                        summary.smart_gym
                          .equipment_count,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <div className="flex items-center gap-3">
                      <Activity
                        size={18}
                        className="text-cyan-300"
                      />

                      <p className="text-sm text-zinc-500">
                        Telemetry samples
                      </p>
                    </div>

                    <p className="mt-3 text-2xl font-semibold">
                      {formatNumber(
                        summary.smart_gym
                          .telemetry_samples,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <div className="flex items-center gap-3">
                      <Bot
                        size={18}
                        className="text-cyan-300"
                      />

                      <p className="text-sm text-zinc-500">
                        Total AI commands
                      </p>
                    </div>

                    <p className="mt-3 text-2xl font-semibold">
                      {formatNumber(
                        summary.smart_gym
                          .total_commands,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <div className="flex items-center gap-3">
                      <Database
                        size={18}
                        className="text-cyan-300"
                      />

                      <p className="text-sm text-zinc-500">
                        Resistance adjustments
                      </p>
                    </div>

                    <p className="mt-3 text-2xl font-semibold">
                      {formatNumber(
                        summary.smart_gym
                          .increase_commands +
                          summary.smart_gym
                            .decrease_commands,
                      )}
                    </p>
                  </div>
                </div>
              </SectionCard>

              <SectionCard
                title="System Health"
                icon={Activity}
              >
                <div className="space-y-3">
                  {[
                    [
                      "Backend API",
                      "Operational",
                    ],
                    [
                      "PostgreSQL",
                      "Connected",
                    ],
                    [
                      "AI services",
                      "Ready",
                    ],
                    [
                      "Smart Gym",
                      "Connected",
                    ],
                  ].map(
                    ([label, status]) => (
                      <div
                        key={label}
                        className="flex items-center justify-between rounded-xl border border-white/5 bg-white/[0.025] px-4 py-3"
                      >
                        <span className="text-sm text-zinc-500">
                          {label}
                        </span>

                        <span className="flex items-center gap-2 text-xs font-medium text-emerald-300">
                          <span className="h-1.5 w-1.5 rounded-full bg-emerald-300 shadow-[0_0_10px_rgba(110,231,183,0.8)]" />
                          {status}
                        </span>
                      </div>
                    ),
                  )}
                </div>
              </SectionCard>
            </section>

            <footer className="mt-8 flex flex-col gap-2 border-t border-white/10 pt-6 text-xs text-zinc-700 sm:flex-row sm:items-center sm:justify-between">
              <span>
                AI Gym & Fitness Assistant
              </span>

              <span>
                Administrator analytics
              </span>
            </footer>
          </>
        ) : null}
      </div>
    </main>
  );
}
