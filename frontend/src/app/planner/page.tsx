"use client";

import {
  CircleAlert,
  Dumbbell,
  Loader2,
  MapPin,
  Sparkles,
  Trophy,
} from "lucide-react";
import { useState } from "react";
import { useRouter } from "next/navigation";

import { PageHeader } from "@/components/page-header";
import {
  ApiError,
  getFitnessRecommendations,
  type FitnessRecommendations,
} from "@/lib/api";

const sampleGyms = [
  {
    name: "Pulse Fitness Studio",
    distance_km: 2.4,
    rating: 4.7,
    specialties: ["strength", "functional training"],
  },
  {
    name: "Momentum Gym",
    distance_km: 4.8,
    rating: 4.5,
    specialties: ["cardio", "group classes"],
  },
  {
    name: "Core Lab",
    distance_km: 7.1,
    rating: 4.8,
    specialties: ["strength", "mobility"],
  },
];

export default function PlannerPage() {
  const router = useRouter();
  const [maxDistance, setMaxDistance] = useState("10");
  const [recommendations, setRecommendations] =
    useState<FitnessRecommendations | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function generatePlan() {
    setLoading(true);
    setErrorMessage("");

    try {
      const distance = Number(maxDistance);
      setRecommendations(
        await getFitnessRecommendations(
          Number.isFinite(distance) ? distance : 10,
          sampleGyms,
        ),
      );
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      setErrorMessage(
        error instanceof ApiError
          ? error.detail
          : "Recommendations are not available right now.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-6xl px-5 py-7 md:px-8 md:py-10">
        <PageHeader
          eyebrow="Recommendation engine"
          title="Fitness planner"
          description="Generate workout programs, challenges, and gym suggestions tailored to your saved fitness goal."
          icon={Sparkles}
        />

        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/5 p-4 text-sm text-red-300">
            <CircleAlert size={18} className="mt-0.5 shrink-0" />
            <p>{errorMessage}</p>
          </div>
        )}

        <section className="mt-8 rounded-3xl border border-cyan-300/15 bg-gradient-to-br from-cyan-400/[0.1] via-[#0d1117] to-[#0b0e13] p-6 md:p-8">
          <div className="grid gap-5 md:grid-cols-[1fr_auto] md:items-end">
            <div>
              <label htmlFor="max-distance" className="text-sm font-medium text-zinc-200">
                Maximum distance for gym suggestions
              </label>
              <p className="mt-1 text-sm text-zinc-500">
                The planner uses three example local facilities; connect location search later to supply real nearby gyms.
              </p>
              <select
                id="max-distance"
                value={maxDistance}
                onChange={(event) => setMaxDistance(event.target.value)}
                className="mt-4 h-11 w-full max-w-xs rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
              >
                <option value="5">Within 5 km</option>
                <option value="10">Within 10 km</option>
                <option value="20">Within 20 km</option>
              </select>
            </div>
            <button
              type="button"
              onClick={() => void generatePlan()}
              disabled={loading}
              className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? <Loader2 size={17} className="animate-spin" /> : <Sparkles size={17} />}
              {loading ? "Creating plan..." : "Generate my plan"}
            </button>
          </div>
        </section>

        {recommendations && (
          <section className="mt-5 grid gap-5 lg:grid-cols-3">
            <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
              <div className="flex items-center gap-3">
                <MapPin size={19} className="text-cyan-300" />
                <div>
                  <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                    Gym matches
                  </p>
                  <h2 className="mt-1 text-lg font-semibold">Nearby options</h2>
                </div>
              </div>
              <div className="mt-5 space-y-4">
                {recommendations.gyms.map((gym) => (
                  <div key={gym.name} className="rounded-2xl bg-white/[0.025] p-4">
                    <p className="font-medium">{gym.name}</p>
                    <p className="mt-1 text-xs text-cyan-300">
                      {gym.distance_km} km · {gym.rating.toFixed(1)} rating
                    </p>
                    <p className="mt-3 text-xs leading-5 text-zinc-500">{gym.reason}</p>
                  </div>
                ))}
              </div>
            </article>

            <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
              <div className="flex items-center gap-3">
                <Dumbbell size={19} className="text-cyan-300" />
                <div>
                  <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                    Program matches
                  </p>
                  <h2 className="mt-1 text-lg font-semibold">Workout ideas</h2>
                </div>
              </div>
              <div className="mt-5 space-y-4">
                {recommendations.workouts.map((workout) => (
                  <div key={workout.name} className="rounded-2xl bg-white/[0.025] p-4">
                    <p className="font-medium">{workout.name}</p>
                    <p className="mt-1 text-xs capitalize text-cyan-300">
                      {workout.difficulty} · {workout.duration_minutes} min
                    </p>
                    <p className="mt-3 text-xs leading-5 text-zinc-500">{workout.reason}</p>
                  </div>
                ))}
              </div>
            </article>

            <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
              <div className="flex items-center gap-3">
                <Trophy size={19} className="text-cyan-300" />
                <div>
                  <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                    Challenge matches
                  </p>
                  <h2 className="mt-1 text-lg font-semibold">Stay consistent</h2>
                </div>
              </div>
              <div className="mt-5 space-y-4">
                {recommendations.challenges.map((challenge) => (
                  <div key={challenge.name} className="rounded-2xl bg-white/[0.025] p-4">
                    <p className="font-medium">{challenge.name}</p>
                    <p className="mt-1 text-xs capitalize text-cyan-300">
                      {challenge.difficulty} · {challenge.duration_days} days
                    </p>
                    <p className="mt-3 text-xs leading-5 text-zinc-500">{challenge.reason}</p>
                  </div>
                ))}
              </div>
            </article>
          </section>
        )}
      </div>
    </main>
  );
}
