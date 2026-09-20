"use client";

import { useRouter } from "next/navigation";
import {
  Camera,
  Check,
  ChevronRight,
  CircleAlert,
  CircleStop,
  Loader2,
  ScanLine,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";

import { AnimatedAIBuddy } from "@/components/animated-ai-buddy";
import { getAccessToken } from "@/lib/auth";
import {
  analyzeLiveTrainerFrame,
  ApiError,
  getCurrentUser,
  startLiveTrainer,
  stopLiveTrainer,
  type CurrentUser,
  type LiveTrainerAnalysis,
  type LiveTrainerLandmark,
} from "@/lib/api";
import { hasCompletedFitnessSetup } from "@/lib/fitness-profile";
import {
  buildTodayPlan,
  type WorkoutExercise,
  type WorkoutPlan,
} from "@/lib/workout-plan";

const FRAME_INTERVAL_MS = 420;
const FORM_PASSING_SCORE = 72;

const POSE_CONNECTIONS = [
  [11, 12],
  [11, 13],
  [13, 15],
  [12, 14],
  [14, 16],
  [11, 23],
  [12, 24],
  [23, 24],
  [23, 25],
  [25, 27],
  [27, 29],
  [29, 31],
  [24, 26],
  [26, 28],
  [28, 30],
  [30, 32],
] as const;

function hasCorrection(analysis: LiveTrainerAnalysis): boolean {
  return (
    analysis.form_score < FORM_PASSING_SCORE ||
    analysis.feedback.some((message) =>
      /shallow|needs improvement|leaning excessively|unstable|keep your/i.test(
        message,
      ),
    )
  );
}

function formMessage(analysis: LiveTrainerAnalysis | null): string {
  if (!analysis) {
    return "Move into view so AI Buddy can find your pose.";
  }

  if (!hasCorrection(analysis)) {
    return "Correct form — keep the movement controlled.";
  }

  return analysis.feedback[0] ?? "Adjust your squat position, then try again.";
}

function storageKey(user: CurrentUser, plan: WorkoutPlan): string {
  return `ai-gym-live-roadmap:${user.id}:${plan.dateKey}`;
}

function chooseFemaleVoice(): SpeechSynthesisVoice | null {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) {
    return null;
  }

  const voices = window.speechSynthesis.getVoices();
  const femaleVoice = voices.find((voice) =>
    /female|zira|samantha|ava|jenny|aria|emma|sonia|heera|hazel/i.test(
      voice.name,
    ),
  );

  return femaleVoice ?? voices.find((voice) => voice.lang.startsWith("en")) ?? null;
}

export default function LiveTrainerPage() {
  const router = useRouter();
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const captureCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const overlayCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const sessionIdRef = useRef<string | null>(null);
  const frameTimerRef = useRef<number | null>(null);
  const frameInFlightRef = useRef(false);
  const liveRef = useRef(false);
  const lastSpokenAtRef = useRef(0);
  const lastSpokenCueRef = useRef("");
  const lastRepAnnouncedRef = useRef(0);

  const [starting, setStarting] = useState(false);
  const [live, setLive] = useState(false);
  const [profileLoading, setProfileLoading] = useState(true);
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [plan, setPlan] = useState<WorkoutPlan>(() => buildTodayPlan(null));
  const [activeExerciseId, setActiveExerciseId] = useState("");
  const [completedExerciseIds, setCompletedExerciseIds] = useState<string[]>([]);
  const [analysis, setAnalysis] = useState<LiveTrainerAnalysis | null>(null);
  const [poseDetected, setPoseDetected] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const activeExercise = useMemo<WorkoutExercise>(
    () =>
      plan.exercises.find((exercise) => exercise.id === activeExerciseId) ??
      plan.exercises[0],
    [activeExerciseId, plan.exercises],
  );
  const cameraSupportsExercise = activeExercise?.kind === "squat";

  function speak(text: string, interrupt = false) {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      return;
    }

    const now = Date.now();
    const cue = text.trim();

    if (
      !cue ||
      (!interrupt &&
        (window.speechSynthesis.speaking ||
          (cue === lastSpokenCueRef.current &&
            now - lastSpokenAtRef.current < 6000)))
    ) {
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(cue);
    const femaleVoice = chooseFemaleVoice();

    if (femaleVoice) {
      utterance.voice = femaleVoice;
    }

    utterance.rate = 1.03;
    utterance.pitch = 1.15;
    utterance.volume = 0.9;
    window.speechSynthesis.speak(utterance);
    lastSpokenCueRef.current = cue;
    lastSpokenAtRef.current = now;
  }

  function clearPoseOverlay() {
    const canvas = overlayCanvasRef.current;
    const context = canvas?.getContext("2d");

    if (canvas && context) {
      context.clearRect(0, 0, canvas.width, canvas.height);
    }
  }

  function drawPoseOverlay(
    landmarks: LiveTrainerLandmark[] | null,
    currentAnalysis: LiveTrainerAnalysis | null,
  ) {
    const canvas = overlayCanvasRef.current;
    const video = videoRef.current;
    const context = canvas?.getContext("2d");

    if (!canvas || !video || !context || !landmarks?.length) {
      clearPoseOverlay();
      return;
    }

    const viewportWidth = canvas.clientWidth;
    const viewportHeight = canvas.clientHeight;
    const sourceWidth = video.videoWidth;
    const sourceHeight = video.videoHeight;

    if (!viewportWidth || !viewportHeight || !sourceWidth || !sourceHeight) {
      return;
    }

    const pixelRatio = window.devicePixelRatio || 1;
    const targetWidth = Math.round(viewportWidth * pixelRatio);
    const targetHeight = Math.round(viewportHeight * pixelRatio);

    if (canvas.width !== targetWidth || canvas.height !== targetHeight) {
      canvas.width = targetWidth;
      canvas.height = targetHeight;
    }

    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    context.clearRect(0, 0, viewportWidth, viewportHeight);

    const scale = Math.max(
      viewportWidth / sourceWidth,
      viewportHeight / sourceHeight,
    );
    const renderedWidth = sourceWidth * scale;
    const renderedHeight = sourceHeight * scale;
    const offsetX = (viewportWidth - renderedWidth) / 2;
    const offsetY = (viewportHeight - renderedHeight) / 2;
    const correct = currentAnalysis ? !hasCorrection(currentAnalysis) : false;
    const color = correct ? "#34d399" : "#fb7185";

    const pointAt = (landmark: LiveTrainerLandmark) => ({
      x: offsetX + landmark.x * renderedWidth,
      y: offsetY + landmark.y * renderedHeight,
    });

    context.lineCap = "round";
    context.lineJoin = "round";
    context.strokeStyle = color;
    context.lineWidth = 5;
    context.shadowColor = color;
    context.shadowBlur = 16;

    POSE_CONNECTIONS.forEach(([fromIndex, toIndex]) => {
      const from = landmarks[fromIndex];
      const to = landmarks[toIndex];

      if (!from || !to || from.visibility < 0.35 || to.visibility < 0.35) {
        return;
      }

      const start = pointAt(from);
      const end = pointAt(to);
      context.beginPath();
      context.moveTo(start.x, start.y);
      context.lineTo(end.x, end.y);
      context.stroke();
    });

    context.fillStyle = color;
    landmarks.forEach((landmark) => {
      if (landmark.visibility < 0.45) {
        return;
      }

      const point = pointAt(landmark);
      context.beginPath();
      context.arc(point.x, point.y, 4.5, 0, Math.PI * 2);
      context.fill();
    });

    context.shadowBlur = 0;
  }

  function clearFrameTimer() {
    if (frameTimerRef.current !== null) {
      window.clearTimeout(frameTimerRef.current);
      frameTimerRef.current = null;
    }
  }

  function stopCameraTracks() {
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    clearPoseOverlay();
  }

  function finishLiveWorkout() {
    const sessionId = sessionIdRef.current;

    liveRef.current = false;
    sessionIdRef.current = null;
    clearFrameTimer();
    stopCameraTracks();
    setLive(false);
    setPoseDetected(false);
    setAnalysis(null);
    window.speechSynthesis?.cancel();

    if (sessionId) {
      void stopLiveTrainer(sessionId).catch(() => undefined);
    }
  }

  useEffect(() => {
    let cancelled = false;

    async function loadWorkoutRoadmap() {
      try {
        const profile = await getCurrentUser();

        if (cancelled) {
          return;
        }

        if (!hasCompletedFitnessSetup(profile)) {
          router.replace("/onboarding");
          return;
        }

        const nextPlan = buildTodayPlan(profile);
        const savedProgress = window.localStorage.getItem(
          storageKey(profile, nextPlan),
        );
        const completed = savedProgress
          ? (JSON.parse(savedProgress) as string[])
          : [];
        const firstRemaining = nextPlan.exercises.find(
          (exercise) => !completed.includes(exercise.id),
        );

        setUser(profile);
        setPlan(nextPlan);
        setCompletedExerciseIds(completed);
        setActiveExerciseId(
          firstRemaining?.id ?? nextPlan.exercises[0].id,
        );
        speak(nextPlan.voiceIntro, true);
      } catch (error) {
        if (cancelled) {
          return;
        }

        if (error instanceof ApiError && error.status === 401) {
          router.replace("/login");
        } else {
          setErrorMessage("Live Trainer is unavailable right now. Please try again.");
        }
      } finally {
        if (!cancelled) {
          setProfileLoading(false);
        }
      }
    }

    void loadWorkoutRoadmap();

    return () => {
      cancelled = true;
    };
  }, [router]);

  useEffect(() => {
    if (!user) {
      return;
    }

    window.localStorage.setItem(
      storageKey(user, plan),
      JSON.stringify(completedExerciseIds),
    );
  }, [completedExerciseIds, plan, user]);

  useEffect(() => {
    const timer = window.setInterval(() => {
      if (!user) {
        return;
      }

      const nextPlan = buildTodayPlan(user);

      if (nextPlan.dateKey !== plan.dateKey) {
        const savedProgress = window.localStorage.getItem(
          storageKey(user, nextPlan),
        );
        const completed = savedProgress
          ? (JSON.parse(savedProgress) as string[])
          : [];
        const firstRemaining = nextPlan.exercises.find(
          (exercise) => !completed.includes(exercise.id),
        );

        finishLiveWorkout();
        setPlan(nextPlan);
        setCompletedExerciseIds(completed);
        setActiveExerciseId(
          firstRemaining?.id ?? nextPlan.exercises[0].id,
        );
      }
    }, 60_000);

    return () => window.clearInterval(timer);
    // The timer reads the current day from the shared plan state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [plan.dateKey, user]);

  function scheduleNextFrame() {
    clearFrameTimer();

    if (!liveRef.current) {
      return;
    }

    frameTimerRef.current = window.setTimeout(() => {
      void captureFrame();
    }, FRAME_INTERVAL_MS);
  }

  function applyFrameResult(
    nextAnalysis: LiveTrainerAnalysis | null,
    landmarks: LiveTrainerLandmark[] | null,
  ) {
    setAnalysis(nextAnalysis);
    drawPoseOverlay(landmarks, nextAnalysis);

    if (!nextAnalysis) {
      return;
    }

    if (hasCorrection(nextAnalysis)) {
      speak(formMessage(nextAnalysis));
      return;
    }

    if (nextAnalysis.repetitions > lastRepAnnouncedRef.current) {
      lastRepAnnouncedRef.current = nextAnalysis.repetitions;
      speak(`Good repetition ${nextAnalysis.repetitions}.`);
    }
  }

  async function captureFrame() {
    const video = videoRef.current;
    const canvas = captureCanvasRef.current;
    const sessionId = sessionIdRef.current;

    if (
      !liveRef.current ||
      frameInFlightRef.current ||
      !video ||
      !canvas ||
      !sessionId ||
      video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA
    ) {
      scheduleNextFrame();
      return;
    }

    const width = Math.min(video.videoWidth || 640, 640);
    const height = Math.round(
      (video.videoHeight || 480) * (width / (video.videoWidth || 640)),
    );

    if (!width || !height) {
      scheduleNextFrame();
      return;
    }

    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext("2d");

    if (!context) {
      setErrorMessage("The camera frame could not be prepared.");
      return;
    }

    context.drawImage(video, 0, 0, width, height);
    frameInFlightRef.current = true;

    canvas.toBlob(
      async (image) => {
        if (!image) {
          frameInFlightRef.current = false;
          scheduleNextFrame();
          return;
        }

        try {
          const frame = await analyzeLiveTrainerFrame(sessionId, image);

          if (!liveRef.current) {
            return;
          }

          setPoseDetected(frame.pose_detected);
          applyFrameResult(frame.analysis, frame.landmarks);

          if (!frame.pose_detected) {
            clearPoseOverlay();
          }

          setErrorMessage("");
        } catch (error) {
          if (error instanceof ApiError && error.status === 401) {
            liveRef.current = false;
            stopCameraTracks();
            router.replace("/login");
            return;
          }

          setErrorMessage(
            error instanceof ApiError
              ? error.detail
              : "Live form analysis is temporarily unavailable.",
          );
        } finally {
          frameInFlightRef.current = false;
          scheduleNextFrame();
        }
      },
      "image/jpeg",
      0.82,
    );
  }

  async function startLiveWorkout() {
    if (starting || liveRef.current || !cameraSupportsExercise) {
      return;
    }

    if (!getAccessToken()) {
      router.replace("/login");
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
      setErrorMessage("This browser does not support camera access.");
      return;
    }

    setStarting(true);
    setErrorMessage("");
    setAnalysis(null);
    setPoseDetected(false);
    lastRepAnnouncedRef.current = 0;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
          facingMode: "user",
          width: { ideal: 640 },
          height: { ideal: 480 },
        },
      });

      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      const session = await startLiveTrainer();
      sessionIdRef.current = session.session_id;
      liveRef.current = true;
      setLive(true);
      speak(
        "Camera connected. Copy the squat demonstration, keep your full body side-on, and I will correct your form.",
        true,
      );
      scheduleNextFrame();
    } catch (error) {
      stopCameraTracks();

      if (error instanceof ApiError && error.status === 401) {
        router.replace("/login");
        return;
      }

      if (error instanceof DOMException && error.name === "NotAllowedError") {
        setErrorMessage("Camera permission was declined. Allow camera access and try again.");
      } else {
        setErrorMessage(
          error instanceof ApiError
            ? error.detail
            : "Unable to start the live camera trainer.",
        );
      }
    } finally {
      setStarting(false);
    }
  }

  function selectExercise(exercise: WorkoutExercise) {
    if (live) {
      finishLiveWorkout();
    }

    setActiveExerciseId(exercise.id);
    speak(`${exercise.name}. ${exercise.prescription}. ${exercise.cue}`, true);
  }

  function toggleExerciseComplete(exercise: WorkoutExercise) {
    setCompletedExerciseIds((current) => {
      const completed = current.includes(exercise.id)
        ? current.filter((id) => id !== exercise.id)
        : [...current, exercise.id];

      if (!current.includes(exercise.id)) {
        const nextExercise = plan.exercises.find(
          (item) => !completed.includes(item.id),
        );

        if (nextExercise) {
          setActiveExerciseId(nextExercise.id);
          speak(
            `${exercise.name} complete. Next, ${nextExercise.name}: ${nextExercise.prescription}. ${nextExercise.cue}`,
            true,
          );
        } else {
          speak("Excellent work. You completed today's workout roadmap.", true);
        }
      }

      return completed;
    });
  }

  useEffect(() => {
    return () => {
      const sessionId = sessionIdRef.current;
      liveRef.current = false;
      clearFrameTimer();
      stopCameraTracks();

      if (sessionId) {
        void stopLiveTrainer(sessionId).catch(() => undefined);
      }
    };
    // The cleanup intentionally uses the latest refs only when unmounting.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const formIsCorrect = analysis ? !hasCorrection(analysis) : false;
  const cameraLabel = !live
    ? "Camera off"
    : !poseDetected
      ? "Finding your body"
      : formIsCorrect
        ? "Correct form"
        : "Adjust your form";
  const completedCount = completedExerciseIds.length;

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="mx-auto w-full max-w-7xl px-5 py-7 md:px-8 md:py-10">
        <div className="mb-6">
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-200/70">Live AI Trainer · Today&apos;s roadmap</p>
          <h1 className="mt-2 text-2xl font-semibold tracking-tight md:text-3xl">Copy AI Buddy. Complete today&apos;s plan.</h1>
        </div>

        {errorMessage && (
          <div className="mb-6 flex items-start gap-3 rounded-2xl border border-red-400/20 bg-red-400/[0.07] p-4 text-sm leading-6 text-red-200">
            <CircleAlert size={18} className="mt-0.5 shrink-0" />
            <p>{errorMessage}</p>
          </div>
        )}

        <section className="grid items-start gap-6 xl:grid-cols-2">
          <article className="overflow-hidden rounded-3xl border border-white/10 bg-[#0b0e13] shadow-2xl shadow-black/20">
            <div className="flex items-center justify-between gap-4 border-b border-white/10 px-5 py-4 md:px-6">
              <div>
                <p className="text-xs font-medium uppercase tracking-[0.16em] text-zinc-500">Your camera</p>
                <h2 className="mt-1 text-lg font-semibold">Live squat form tracking</h2>
              </div>
              <span className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium ${live ? (poseDetected ? (formIsCorrect ? "border-emerald-300/30 bg-emerald-300/10 text-emerald-200" : "border-rose-300/30 bg-rose-300/10 text-rose-200") : "border-amber-300/30 bg-amber-300/10 text-amber-100") : "border-white/10 bg-white/5 text-zinc-400"}`}>
                <span className={`h-1.5 w-1.5 rounded-full ${live ? (poseDetected ? (formIsCorrect ? "bg-emerald-300" : "bg-rose-300") : "bg-amber-300") : "bg-zinc-500"}`} />
                {cameraLabel}
              </span>
            </div>

            <div className="relative aspect-[4/3] overflow-hidden bg-[#030609]">
              <video ref={videoRef} muted playsInline className={`h-full w-full object-cover ${live ? "block" : "hidden"}`} />
              <canvas ref={captureCanvasRef} className="hidden" />
              <canvas ref={overlayCanvasRef} aria-label="Live pose skeleton showing whether squat form is correct" className="pointer-events-none absolute inset-0 h-full w-full" />

              {!live && (
                <div className="absolute inset-0 flex flex-col items-center justify-center px-8 text-center">
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-200">
                    <ScanLine size={25} />
                  </div>
                  <p className="mt-4 text-base font-medium text-zinc-100">Your squat form will be tracked here</p>
                  <p className="mt-2 max-w-sm text-sm leading-6 text-zinc-500">Choose a squat in today&apos;s roadmap, stand side-on with your full body in view, then copy AI Buddy.</p>
                </div>
              )}

              {live && (
                <div className={`pointer-events-none absolute inset-x-4 bottom-4 rounded-2xl border px-4 py-3 backdrop-blur ${poseDetected ? (formIsCorrect ? "border-emerald-300/30 bg-emerald-950/75 text-emerald-100" : "border-rose-300/30 bg-rose-950/75 text-rose-100") : "border-amber-300/25 bg-black/70 text-amber-100"}`}>
                  <p className="text-sm font-medium" aria-live="polite">{poseDetected ? formMessage(analysis) : "Move back until your full body is visible from the side."}</p>
                </div>
              )}
            </div>

            <div className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center sm:justify-between md:px-6">
              <p className="text-xs leading-5 text-zinc-500">Green lines mean correct form. Red lines show an AI Buddy correction. Squat tracking is available when a squat is selected.</p>
              {live ? (
                <button type="button" onClick={finishLiveWorkout} className="inline-flex h-11 shrink-0 items-center justify-center gap-2 rounded-xl border border-rose-300/25 bg-rose-300/10 px-4 text-sm font-medium text-rose-100 transition hover:bg-rose-300/15">
                  <CircleStop size={17} />
                  Stop camera
                </button>
              ) : (
                <button type="button" onClick={() => void startLiveWorkout()} disabled={starting || profileLoading || !cameraSupportsExercise} className="inline-flex h-11 shrink-0 items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50">
                  {starting || profileLoading ? <><Loader2 size={17} className="animate-spin" /> Starting...</> : cameraSupportsExercise ? <><Camera size={17} /> Start squat camera</> : <>Choose a squat</>}
                </button>
              )}
            </div>
          </article>

          <article className="overflow-hidden rounded-3xl border border-cyan-300/20 bg-[#090d12] shadow-2xl shadow-cyan-950/10">
            <div className="flex flex-wrap items-center justify-between gap-3 border-b border-cyan-300/15 px-5 py-4 md:px-6">
              <div>
                <p className="text-xs font-medium uppercase tracking-[0.16em] text-cyan-200/70">Female AI Buddy</p>
                <h2 className="mt-1 text-lg font-semibold">{activeExercise.name}</h2>
              </div>
              <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1.5 text-xs font-medium text-cyan-100">{activeExercise.prescription}</span>
            </div>

            <AnimatedAIBuddy exercise={activeExercise} />

            <div className="border-t border-cyan-300/15 p-5 md:p-6">
              <div className="flex items-end justify-between gap-4">
                <div>
                  <p className="text-xs font-medium uppercase tracking-[0.16em] text-zinc-500">Today&apos;s roadmap</p>
                  <h3 className="mt-1 text-base font-semibold">{plan.focus}</h3>
                </div>
                <span className="text-sm font-medium text-cyan-100">{completedCount}/{plan.exercises.length} done</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-zinc-400">{activeExercise.cue}</p>

              <div className="mt-4 space-y-2">
                {plan.exercises.map((exercise, index) => {
                  const complete = completedExerciseIds.includes(exercise.id);
                  const active = activeExercise.id === exercise.id;

                  return (
                    <div key={exercise.id} className={`flex items-center gap-3 rounded-2xl border p-3 transition ${active ? "border-cyan-300/35 bg-cyan-300/[0.09]" : "border-white/10 bg-white/[0.025]"}`}>
                      <button type="button" onClick={() => selectExercise(exercise)} className="flex min-w-0 flex-1 items-center gap-3 text-left">
                        <span className={`flex h-7 w-7 shrink-0 items-center justify-center rounded-full text-xs font-bold ${complete ? "bg-emerald-300 text-black" : active ? "bg-cyan-300 text-black" : "bg-white/10 text-zinc-300"}`}>{complete ? <Check size={15} strokeWidth={3} /> : index + 1}</span>
                        <span className="min-w-0"><span className="block truncate text-sm font-medium text-zinc-100">{exercise.name}</span><span className="block text-xs text-zinc-500">{exercise.prescription}</span></span>
                        {!complete && <ChevronRight size={16} className="ml-auto shrink-0 text-zinc-500" />}
                      </button>
                      <button type="button" onClick={() => toggleExerciseComplete(exercise)} aria-pressed={complete} className={`shrink-0 rounded-lg px-3 py-2 text-xs font-semibold transition ${complete ? "bg-emerald-300/15 text-emerald-100 hover:bg-emerald-300/20" : "border border-white/10 bg-white/[0.05] text-zinc-200 hover:bg-white/10"}`}>{complete ? "Done" : "Mark done"}</button>
                    </div>
                  );
                })}
              </div>
            </div>
          </article>
        </section>
      </div>
    </main>
  );
}
