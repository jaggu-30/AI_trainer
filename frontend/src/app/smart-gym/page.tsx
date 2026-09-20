"use client";

import {
  Activity,
  CircleAlert,
  Cpu,
  RefreshCw,
  Signal,
  Watch,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import {
  ApiError,
  getSmartGymStatus,
  type SmartGymStatus,
} from "@/lib/api";

function metric(value: number, suffix = ""): string {
  return `${Number.isInteger(value) ? value : value.toFixed(1)}${suffix}`;
}

export default function SmartGymPage() {
  const router = useRouter();
  const [status, setStatus] = useState<SmartGymStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadStatus(showRefreshState = false) {
    if (showRefreshState) {
      setRefreshing(true);
    }

    setErrorMessage("");

    try {
      setStatus(await getSmartGymStatus());
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Smart Gym telemetry is not available right now.",
      );
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadInitialStatus() {
      try {
        const result = await getSmartGymStatus();
        if (!cancelled) {
          setStatus(result);
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
            : "Smart Gym telemetry is not available right now.",
        );
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    void loadInitialStatus();

    return () => {
      cancelled = true;
    };
  }, [router]);

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-6xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="AI + IoT"
          title="Smart Gym"
          description="See the latest equipment signals and the AI adjustments produced from live gym telemetry."
          icon={Watch}
          action={
            <button
              type="button"
              onClick={() => void loadStatus(true)}
              disabled={loading || refreshing}
              className="inline-flex h-11 items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/5 px-4 text-sm font-medium text-zinc-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCw
                size={16}
                className={refreshing ? "animate-spin" : ""}
              />
              {refreshing ? "Refreshing..." : "Refresh telemetry"}
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
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {[1, 2].map((item) => (
              <div
                key={item}
                className="h-64 animate-pulse rounded-3xl border border-white/10 bg-white/[0.025]"
              />
            ))}
          </div>
        ) : status ? (
          <>
            <section className="mt-8 grid gap-4 sm:grid-cols-3">
              <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5">
                <Signal size={19} className="text-cyan-300" />
                <p className="mt-4 text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Connection
                </p>
                <p
                  className={`mt-2 text-xl font-semibold ${
                    status.mqtt_connected ? "text-emerald-300" : "text-amber-300"
                  }`}
                >
                  {status.mqtt_connected ? "Connected" : "Standing by"}
                </p>
              </article>

              <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5">
                <Cpu size={19} className="text-cyan-300" />
                <p className="mt-4 text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Equipment
                </p>
                <p className="mt-2 text-xl font-semibold">
                  {status.equipment_count} devices
                </p>
              </article>

              <article className="rounded-2xl border border-white/10 bg-[#0b0e13] p-5">
                <Activity size={19} className="text-cyan-300" />
                <p className="mt-4 text-xs uppercase tracking-[0.16em] text-zinc-600">
                  AI control
                </p>
                <p className="mt-2 text-xl font-semibold text-cyan-300">
                  Monitoring
                </p>
              </article>
            </section>

            {status.equipment.length === 0 ? (
              <section className="mt-5 rounded-3xl border border-dashed border-white/15 bg-white/[0.02] px-6 py-14 text-center">
                <Watch size={28} className="mx-auto text-zinc-600" />
                <h2 className="mt-4 text-lg font-semibold">
                  No equipment connected yet
                </h2>
                <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-zinc-500">
                  Start the included Smart Gym simulator or connect an MQTT device to see its latest performance, heart-rate, fatigue, and resistance signals here.
                </p>
              </section>
            ) : (
              <section className="mt-5 grid gap-4 lg:grid-cols-2">
                {status.equipment.map((equipment) => (
                  <article
                    key={equipment.equipment_id}
                    className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                          {equipment.equipment_type}
                        </p>
                        <h2 className="mt-2 text-lg font-semibold">
                          {equipment.equipment_id}
                        </h2>
                      </div>
                      <span className="rounded-full border border-emerald-400/15 bg-emerald-400/5 px-3 py-1.5 text-xs text-emerald-300">
                        Live
                      </span>
                    </div>

                    <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
                      {[
                        ["Resistance", metric(equipment.resistance_level)],
                        ["Repetitions", metric(equipment.repetitions)],
                        ["Performance", metric(equipment.performance_score, "%")],
                        ["Heart rate", metric(equipment.heart_rate, " bpm")],
                      ].map(([label, value]) => (
                        <div
                          key={label}
                          className="rounded-xl bg-white/[0.025] p-3"
                        >
                          <p className="text-[11px] text-zinc-600">{label}</p>
                          <p className="mt-1 text-sm font-medium">{value}</p>
                        </div>
                      ))}
                    </div>

                    <div className="mt-5 rounded-2xl border border-cyan-300/10 bg-cyan-300/[0.04] p-4">
                      <p className="text-xs font-medium text-cyan-200">
                        Latest AI action
                      </p>
                      <p className="mt-2 text-sm capitalize text-zinc-200">
                        {equipment.last_action ?? "No adjustment recommended"}
                      </p>
                      {equipment.last_command_reason && (
                        <p className="mt-1 text-xs leading-5 text-zinc-500">
                          {equipment.last_command_reason}
                        </p>
                      )}
                    </div>
                  </article>
                ))}
              </section>
            )}
          </>
        ) : null}
      </div>
    </main>
  );
}
