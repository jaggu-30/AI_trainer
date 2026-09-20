"use client";

import {
  Activity,
  ArrowLeft,
  Award,
  Camera,
  CheckCircle2,
  Dumbbell,
  FileVideo,
  Gauge,
  Loader2,
  PlayCircle,
  ShieldCheck,
  Sparkles,
  Target,
  Upload,
  XCircle,
} from "lucide-react";
import Link from "next/link";
import {
  ChangeEvent,
  useEffect,
  useState,
} from "react";
import { useRouter } from "next/navigation";

import {
  analyzeGymTrainerPerformanceVideo,
  ApiError,
  getGymTrainerHealth,
  type GymTrainerPerformanceVideo,
} from "@/lib/api";

const exercises = [
  {
    value: "squat",
    label: "Squat",
  },
];

const allowedExtensions = [
  ".mp4",
  ".mov",
  ".avi",
  ".mkv",
];

function scoreColor(
  score: number,
): string {
  if (score >= 90) {
    return "text-emerald-300";
  }

  if (score >= 75) {
    return "text-cyan-300";
  }

  if (score >= 60) {
    return "text-amber-300";
  }

  return "text-red-300";
}

function formatPercent(
  value: number,
): string {
  return `${value.toFixed(1)}%`;
}

function formatDetectionRate(
  value: number,
): string {
  return `${(value * 100).toFixed(1)}%`;
}

function formatDate(
  value: string,
): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}

function ScoreCard({
  label,
  score,
}: {
  label: string;
  score: number;
}) {
  return (
    <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
      <div className="flex items-center justify-between gap-3">
        <p className="text-xs text-zinc-600">
          {label}
        </p>

        <p
          className={`text-sm font-semibold ${scoreColor(
            score,
          )}`}
        >
          {formatPercent(score)}
        </p>
      </div>

      <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-white/5">
        <div
          className="h-full rounded-full bg-cyan-400 transition-all"
          style={{
            width: `${Math.min(
              Math.max(score, 0),
              100,
            )}%`,
          }}
        />
      </div>
    </div>
  );
}

export default function TrainerPage() {
  const router = useRouter();

  const [exercise, setExercise] =
    useState("squat");

  const [selectedFile, setSelectedFile] =
    useState<File | null>(null);

  const [result, setResult] =
    useState<GymTrainerPerformanceVideo | null>(
      null,
    );

  const [loading, setLoading] =
    useState(false);

  const [checkingHealth, setCheckingHealth] =
    useState(true);

  const [serviceHealthy, setServiceHealthy] =
    useState(false);

  const [errorMessage, setErrorMessage] =
    useState("");

  const [dragActive, setDragActive] =
    useState(false);

  useEffect(() => {
    let cancelled = false;

    async function checkService() {
      try {
        await getGymTrainerHealth();

        if (!cancelled) {
          setServiceHealthy(true);
        }
      } catch {
        if (!cancelled) {
          setServiceHealthy(false);
        }
      } finally {
        if (!cancelled) {
          setCheckingHealth(false);
        }
      }
    }

    void checkService();

    return () => {
      cancelled = true;
    };
  }, []);

  function validateFile(
    file: File,
  ): boolean {
    const lowerName =
      file.name.toLowerCase();

    const supported =
      allowedExtensions.some(
        (extension) =>
          lowerName.endsWith(extension),
      );

    if (!supported) {
      setErrorMessage(
        "Unsupported video format. Use MP4, MOV, AVI, or MKV.",
      );
      return false;
    }

    setErrorMessage("");
    return true;
  }

  function selectFile(
    file: File,
  ) {
    if (!validateFile(file)) {
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setErrorMessage("");
  }

  function handleFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    const file =
      event.target.files?.[0];

    if (file) {
      selectFile(file);
    }
  }

  function handleDrop(
    event: React.DragEvent<HTMLLabelElement>,
  ) {
    event.preventDefault();
    setDragActive(false);

    const file =
      event.dataTransfer.files?.[0];

    if (file) {
      selectFile(file);
    }
  }

  async function handleAnalyze() {
    if (!selectedFile) {
      setErrorMessage(
        "Select a recorded workout video first.",
      );
      return;
    }

    setLoading(true);
    setErrorMessage("");
    setResult(null);

    try {
      const analysis =
        await analyzeGymTrainerPerformanceVideo(
          selectedFile,
          exercise,
        );

      setResult(analysis);
    } catch (error) {
      if (error instanceof ApiError) {
        if (error.status === 401) {
          router.replace("/login");
          return;
        }

        setErrorMessage(
          error.detail,
        );
      } else {
        setErrorMessage(
          "Video performance analysis failed. Please try again.",
        );
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-7xl px-5 py-7 md:px-8 md:py-10">
        <header className="flex flex-col gap-5 border-b border-white/10 pb-7 md:flex-row md:items-end md:justify-between">
          <div>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 text-xs text-zinc-600 transition hover:text-cyan-300"
            >
              <ArrowLeft size={14} />
              Back to dashboard
            </Link>

            <div className="mt-5 flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-400 text-black shadow-[0_0_35px_rgba(34,211,238,0.25)]">
                <Dumbbell size={22} />
              </div>

              <div>
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-cyan-300">
                  AI Gym
                </p>

                <h1 className="mt-1 text-2xl font-semibold tracking-tight md:text-3xl">
                  AI Trainer
                </h1>
              </div>
            </div>

            <p className="mt-4 max-w-2xl text-sm leading-6 text-zinc-500">
              Upload a recorded workout and receive a complete
              AI-generated performance report with repetition-level
              scoring.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/live-trainer"
              className="inline-flex h-10 items-center gap-2 rounded-xl bg-cyan-400 px-4 text-xs font-semibold text-black transition hover:bg-cyan-300"
            >
              <Camera size={15} />
              Live camera
            </Link>

            <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.025] px-3 py-2 text-xs">
              {checkingHealth ? (
                <>
                  <Loader2
                    size={14}
                    className="animate-spin text-zinc-500"
                  />
                  <span className="text-zinc-600">
                    Checking trainer
                  </span>
                </>
              ) : serviceHealthy ? (
                <>
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-300 shadow-[0_0_10px_rgba(110,231,183,0.8)]" />
                  <span className="text-emerald-300">
                    Trainer online
                  </span>
                </>
              ) : (
                <>
                  <span className="h-1.5 w-1.5 rounded-full bg-red-300" />
                  <span className="text-red-300">
                    Trainer unavailable
                  </span>
                </>
              )}
            </div>
          </div>
        </header>

        {errorMessage && (
          <div className="mt-6 flex items-start gap-3 rounded-2xl border border-red-400/15 bg-red-400/5 p-4 text-sm leading-6 text-red-300">
            <XCircle
              size={18}
              className="mt-0.5 shrink-0"
            />

            <div>
              <p className="font-medium">
                Analysis error
              </p>

              <p className="mt-1 text-red-300/80">
                {errorMessage}
              </p>
            </div>
          </div>
        )}

        <section className="mt-8 grid gap-6 xl:grid-cols-[0.82fr_1.18fr]">
          <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
            <div className="flex items-start gap-4">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-300/10 bg-cyan-300/5 text-cyan-300">
                <FileVideo size={19} />
              </div>

              <div>
                <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Performance analysis
                </p>

                <h2 className="mt-2 text-xl font-semibold">
                  Upload workout video
                </h2>

                <p className="mt-2 text-xs leading-5 text-zinc-600">
                  The completed analysis is saved to your workout
                  history.
                </p>
              </div>
            </div>

            <div className="mt-7">
              <label
                htmlFor="exercise"
                className="mb-2 block text-sm font-medium text-zinc-300"
              >
                Exercise
              </label>

              <select
                id="exercise"
                value={exercise}
                onChange={(event) =>
                  setExercise(
                    event.target.value,
                  )
                }
                className="h-12 w-full rounded-xl border border-white/10 bg-[#090b0f] px-4 text-sm text-white outline-none transition focus:border-cyan-300/30 focus:ring-2 focus:ring-cyan-300/10"
              >
                {exercises.map(
                  (item) => (
                    <option
                      key={item.value}
                      value={item.value}
                    >
                      {item.label}
                    </option>
                  ),
                )}
              </select>
            </div>

            <label
              htmlFor="workout-video"
              onDragOver={(event) => {
                event.preventDefault();
                setDragActive(true);
              }}
              onDragLeave={() =>
                setDragActive(false)
              }
              onDrop={handleDrop}
              className={`mt-5 flex min-h-56 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed p-6 text-center transition ${
                dragActive
                  ? "border-cyan-300/60 bg-cyan-300/10"
                  : "border-white/10 bg-white/[0.02] hover:border-cyan-300/20 hover:bg-white/[0.035]"
              }`}
            >
              <input
                id="workout-video"
                type="file"
                accept=".mp4,.mov,.avi,.mkv,video/mp4,video/quicktime,video/x-msvideo,video/x-matroska"
                onChange={handleFileChange}
                className="sr-only"
              />

              <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300">
                <Upload size={20} />
              </div>

              <p className="mt-4 text-sm font-medium">
                {selectedFile
                  ? selectedFile.name
                  : "Drop a recorded workout video here"}
              </p>

              <p className="mt-2 text-xs text-zinc-600">
                or click to browse your files
              </p>

              {selectedFile && (
                <p className="mt-3 text-xs text-cyan-300">
                  {(
                    selectedFile.size /
                    1024 /
                    1024
                  ).toFixed(2)}{" "}
                  MB selected
                </p>
              )}
            </label>

            <button
              type="button"
              onClick={() =>
                void handleAnalyze()
              }
              disabled={
                loading ||
                !selectedFile ||
                !serviceHealthy
              }
              className="mt-5 flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading ? (
                <>
                  <Loader2
                    size={17}
                    className="animate-spin"
                  />
                  Generating performance report...
                </>
              ) : (
                <>
                  <PlayCircle size={17} />
                  Analyze workout
                </>
              )}
            </button>

            <div className="mt-5 rounded-2xl border border-white/5 bg-white/[0.02] p-4">
              <div className="flex items-start gap-3">
                <Sparkles
                  size={16}
                  className="mt-0.5 shrink-0 text-cyan-300"
                />

                <p className="text-xs leading-5 text-zinc-600">
                  The uploaded recording is analyzed by the
                  existing AI Trainer pipeline and the completed
                  workout report is persisted by the backend.
                </p>
              </div>
            </div>
          </article>

          <article className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                  Official AI report
                </p>

                <h2 className="mt-2 text-xl font-semibold">
                  Performance results
                </h2>
              </div>

              {result && (
                <span className="rounded-full border border-emerald-400/10 bg-emerald-400/5 px-3 py-1.5 text-xs text-emerald-300">
                  Saved
                </span>
              )}
            </div>

            {!result ? (
              <div className="flex min-h-[580px] flex-col items-center justify-center text-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-3xl border border-white/10 bg-white/[0.025] text-zinc-700">
                  <Gauge size={25} />
                </div>

                <h3 className="mt-5 text-lg font-medium text-zinc-400">
                  Your performance report will appear here
                </h3>

                <p className="mt-2 max-w-sm text-xs leading-6 text-zinc-700">
                  Upload the recorded test video to generate
                  the official session-level performance report.
                </p>
              </div>
            ) : (
              <div className="mt-7 space-y-6">
                <section className="rounded-3xl border border-cyan-300/15 bg-gradient-to-br from-cyan-400/[0.08] to-transparent p-6">
                  <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-[0.16em] text-zinc-600">
                        Overall performance
                      </p>

                      <div className="mt-2 flex items-end gap-3">
                        <span
                          className={`text-5xl font-semibold tracking-tight ${scoreColor(
                            result.performance_score,
                          )}`}
                        >
                          {formatPercent(
                            result.performance_score,
                          )}
                        </span>

                        <span className="mb-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs capitalize text-zinc-400">
                          {result.rating}
                        </span>
                      </div>

                      <p className="mt-3 text-xs text-zinc-600">
                        Official session performance score
                      </p>
                    </div>

                    <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-300/10 bg-cyan-300/5 text-cyan-300">
                      <Award size={28} />
                    </div>
                  </div>
                </section>

                <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <p className="text-xs text-zinc-600">
                      Repetitions
                    </p>

                    <p className="mt-2 text-2xl font-semibold">
                      {result.total_repetitions}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <p className="text-xs text-zinc-600">
                      Best frame
                    </p>

                    <p className="mt-2 text-2xl font-semibold text-emerald-300">
                      {formatPercent(
                        result.best_frame_score,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <p className="text-xs text-zinc-600">
                      Worst frame
                    </p>

                    <p className="mt-2 text-2xl font-semibold">
                      {formatPercent(
                        result.worst_frame_score,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                    <p className="text-xs text-zinc-600">
                      Detection
                    </p>

                    <p className="mt-2 text-2xl font-semibold text-cyan-300">
                      {formatDetectionRate(
                        result.video.detection_rate,
                      )}
                    </p>
                  </div>
                </section>

                <section>
                  <div className="flex items-center gap-3">
                    <Target
                      size={18}
                      className="text-cyan-300"
                    />

                    <div>
                      <p className="text-xs text-zinc-600">
                        Exercise
                      </p>

                      <p className="mt-1 text-lg font-semibold capitalize">
                        {result.exercise.replace(
                          /_/g,
                          " ",
                        )}
                      </p>
                    </div>
                  </div>

                  <div className="mt-5 grid gap-3 sm:grid-cols-3">
                    <ScoreCard
                      label="Depth"
                      score={result.depth_score}
                    />

                    <ScoreCard
                      label="Posture"
                      score={result.posture_score}
                    />

                    <ScoreCard
                      label="Control"
                      score={result.control_score}
                    />
                  </div>
                </section>

                <section>
                  <div className="flex items-center gap-3">
                    <Activity
                      size={18}
                      className="text-cyan-300"
                    />

                    <div>
                      <p className="text-xs uppercase tracking-[0.14em] text-zinc-600">
                        Repetition analysis
                      </p>

                      <h3 className="mt-1 text-base font-semibold">
                        Per-repetition performance
                      </h3>
                    </div>
                  </div>

                  <div className="mt-4 space-y-3">
                    {result.repetition_scores.map(
                      (repetition) => (
                        <div
                          key={
                            repetition.repetition_number
                          }
                          className="rounded-2xl border border-white/5 bg-white/[0.02] p-4"
                        >
                          <div className="flex items-center justify-between gap-4">
                            <div className="flex items-center gap-3">
                              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-300/5 text-sm font-semibold text-cyan-300">
                                {repetition.repetition_number}
                              </div>

                              <div>
                                <p className="text-sm font-medium">
                                  Repetition{" "}
                                  {
                                    repetition.repetition_number
                                  }
                                </p>

                                <p className="mt-1 text-xs capitalize text-zinc-600">
                                  {repetition.rating}
                                </p>
                              </div>
                            </div>

                            <span
                              className={`text-sm font-semibold ${scoreColor(
                                repetition.overall_score,
                              )}`}
                            >
                              {formatPercent(
                                repetition.overall_score,
                              )}
                            </span>
                          </div>

                          <div className="mt-4 grid gap-2 sm:grid-cols-3">
                            <ScoreCard
                              label="Depth"
                              score={
                                repetition.depth_score
                              }
                            />

                            <ScoreCard
                              label="Posture"
                              score={
                                repetition.posture_score
                              }
                            />

                            <ScoreCard
                              label="Control"
                              score={
                                repetition.control_score
                              }
                            />
                          </div>
                        </div>
                      ),
                    )}
                  </div>
                </section>

                <section className="grid gap-4 sm:grid-cols-3">
                  <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">
                    <p className="text-xs text-zinc-600">
                      Average repetition
                    </p>

                    <p className="mt-2 text-lg font-semibold">
                      {formatPercent(
                        result.average_repetition_score,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">
                    <p className="text-xs text-zinc-600">
                      Best repetition
                    </p>

                    <p className="mt-2 text-lg font-semibold text-emerald-300">
                      {formatPercent(
                        result.best_repetition_score,
                      )}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">
                    <p className="text-xs text-zinc-600">
                      Worst repetition
                    </p>

                    <p className="mt-2 text-lg font-semibold">
                      {formatPercent(
                        result.worst_repetition_score,
                      )}
                    </p>
                  </div>
                </section>

                {result.warnings.length > 0 && (
                  <section className="rounded-2xl border border-amber-300/10 bg-amber-300/[0.035] p-5">
                    <div className="flex items-center gap-3">
                      <ShieldCheck
                        size={17}
                        className="text-amber-300"
                      />

                      <h3 className="text-sm font-semibold">
                        AI warnings
                      </h3>
                    </div>

                    <div className="mt-4 space-y-2">
                      {result.warnings.map(
                        (warning) => (
                          <div
                            key={warning}
                            className="flex items-start gap-3 rounded-xl border border-white/5 bg-black/10 px-4 py-3"
                          >
                            <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-300" />

                            <p className="text-xs leading-5 text-zinc-500">
                              {warning}
                            </p>
                          </div>
                        ),
                      )}
                    </div>
                  </section>
                )}

                <section className="rounded-2xl border border-emerald-300/10 bg-emerald-300/[0.025] p-5">
                  <div className="flex items-center gap-3">
                    <CheckCircle2
                      size={18}
                      className="text-emerald-300"
                    />

                    <div>
                      <p className="text-sm font-medium">
                        Workout saved successfully
                      </p>

                      <p className="mt-1 text-xs text-zinc-600">
                        Workout ID: {result.workout.id}
                      </p>
                    </div>
                  </div>

                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    <div>
                      <p className="text-[10px] uppercase tracking-[0.12em] text-zinc-700">
                        Started
                      </p>

                      <p className="mt-1 text-xs text-zinc-500">
                        {formatDate(
                          result.workout.started_at,
                        )}
                      </p>
                    </div>

                    <div>
                      <p className="text-[10px] uppercase tracking-[0.12em] text-zinc-700">
                        Completed
                      </p>

                      <p className="mt-1 text-xs text-zinc-500">
                        {formatDate(
                          result.workout.completed_at,
                        )}
                      </p>
                    </div>
                  </div>
                </section>
              </div>
            )}
          </article>
        </section>
      </div>
    </main>
  );
}
