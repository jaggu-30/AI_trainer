"use client";

import {
  Apple,
  Bot,
  Calculator,
  CheckCircle2,
 
  ClipboardList,
  Coffee,
  Dumbbell,
  Droplets,
  Flame,
  Gauge,
  GlassWater,
  HeartPulse,
  History,
  Leaf,
  Loader2,
  MessageCircle,
  Package,
  RefreshCw,
  Send,
  ShoppingBasket,
  Sparkles,
  Target,
  Utensils,
  XCircle,
} from "lucide-react";
import { FormEvent, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { getCurrentUser } from "@/lib/api";
import type { CurrentUser } from "@/lib/api";
import {
  calculateDieticianTargets,
  createNutritionLog,
  generateDietPlan,
  getDieticianHealth,
  getNutritionHistory,
  getNutritionSummary,
  sendDieticianChat,
  type DieticianCalculationResponse,
  type DietPlanResponse,
  type NutritionLogResponse,
  type NutritionSummaryResponse,
} from "@/lib/dieticianApi";

type TabName = "overview" | "plan" | "nutrition" | "coach";

const activityOptions = [
  { value: "sedentary", label: "Sedentary" },
  { value: "light", label: "Lightly Active" },
  { value: "moderate", label: "Moderately Active" },
  { value: "active", label: "Active" },
  { value: "very_active", label: "Very Active" },
  { value: "extra_active", label: "Extra Active" },
];

const goalOptions = [
  { value: "weight_loss", label: "Weight Loss" },
  { value: "weight_gain", label: "Weight Gain" },
  { value: "muscle_gain", label: "Muscle Gain" },
  { value: "maintenance", label: "Maintain Weight" },
];

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 1,
  }).format(value);
}

function formatDate(value: string) {
  return new Date(value).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function getGoalLabel(goal?: string | null) {
  return (
    goalOptions.find((item) => item.value === goal)?.label ||
    goal ||
    "Not set"
  );
}

function getActivityLabel(activity?: string | null) {
  return (
    activityOptions.find((item) => item.value === activity)?.label ||
    activity ||
    "Not set"
  );
}

function getBmiTone(category: string) {
  const normalized = category.toLowerCase();

  if (normalized.includes("normal")) {
    return "border-emerald-400/20 bg-emerald-400/10 text-emerald-300";
  }

  if (
    normalized.includes("over") ||
    normalized.includes("under") ||
    normalized.includes("obese")
  ) {
    return "border-amber-400/20 bg-amber-400/10 text-amber-300";
  }

  return "border-cyan-400/20 bg-cyan-400/10 text-cyan-300";
}

function StatCard({
  label,
  value,
  suffix,
  icon: Icon,
}: {
  label: string;
  value: string;
  suffix?: string;
  icon: typeof Flame;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/[0.035] p-5 backdrop-blur-xl">
      <div className="mb-4 flex items-center justify-between">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/10">
          <Icon size={20} className="text-cyan-300" />
        </div>
        <span className="text-xs uppercase tracking-[0.16em] text-slate-500">
          Live
        </span>
      </div>

      <div className="text-2xl font-semibold text-white">
        {value}
        {suffix && (
          <span className="ml-1 text-sm font-normal text-slate-400">
            {suffix}
          </span>
        )}
      </div>

      <div className="mt-1 text-sm text-slate-400">{label}</div>
    </div>
  );
}

export default function DieticianPage() {
  const router = useRouter();

  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [activeTab, setActiveTab] = useState<TabName>("overview");

  const [age, setAge] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [activityLevel, setActivityLevel] = useState("moderate");
  const [goal, setGoal] = useState("weight_loss");

  const [calculation, setCalculation] =
    useState<DieticianCalculationResponse | null>(null);

  const [dietPlan, setDietPlan] = useState<DietPlanResponse | null>(null);

  const [nutritionSummary, setNutritionSummary] =
    useState<NutritionSummaryResponse | null>(null);

  const [nutritionHistory, setNutritionHistory] = useState<
    NutritionLogResponse[]
  >([]);

  const [foodName, setFoodName] = useState("");
  const [foodQuantity, setFoodQuantity] = useState("1");
  const [foodCalories, setFoodCalories] = useState("");
  const [foodProtein, setFoodProtein] = useState("");
  const [foodCarbs, setFoodCarbs] = useState("");
  const [foodFat, setFoodFat] = useState("");

  const [chatMessage, setChatMessage] = useState("");
  const [chatResponse, setChatResponse] = useState("");
  const [chatSessionId, setChatSessionId] = useState<number | null>(null);

  const [loadingProfile, setLoadingProfile] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [generatingPlan, setGeneratingPlan] = useState(false);
  const [loggingFood, setLoggingFood] = useState(false);
  const [loadingNutrition, setLoadingNutrition] = useState(false);
  const [sendingChat, setSendingChat] = useState(false);
  const [serviceOnline, setServiceOnline] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadPage() {
      try {
        setLoadingProfile(true);

        const user = await getCurrentUser();

        if (cancelled) {
          return;
        }

        setCurrentUser(user);
        setAge(user.age ? String(user.age) : "");
        setHeight(user.height_cm ? String(user.height_cm) : "");
        setWeight(user.weight_kg ? String(user.weight_kg) : "");
        setActivityLevel(user.activity_level || "moderate");
        setGoal(user.fitness_goal || "weight_loss");

        const [health, summary, history] = await Promise.all([
          getDieticianHealth(),
          getNutritionSummary(),
          getNutritionHistory(20, 0),
        ]);

        if (cancelled) {
          return;
        }

        setServiceOnline(health.status === "healthy");
        setNutritionSummary(summary);
        setNutritionHistory(history);
      } catch (requestError) {
        if (cancelled) {
          return;
        }

        const message =
          requestError instanceof Error
            ? requestError.message
            : "Unable to load the Dietician module.";

        if (
          message.includes("401") ||
          message.toLowerCase().includes("authentication")
        ) {
          router.replace("/login");
          return;
        }

        setError(message);
      } finally {
        if (!cancelled) {
          setLoadingProfile(false);
        }
      }
    }

    loadPage();

    return () => {
      cancelled = true;
    };
  }, [router]);

  const averageDailyCalories = useMemo(() => {
    if (!nutritionSummary || nutritionSummary.total_entries === 0) {
      return 0;
    }

    return nutritionSummary.total_calories;
  }, [nutritionSummary]);

  const remainingCalories = useMemo(() => {
    if (!calculation || !nutritionSummary) {
      return null;
    }

    return Math.max(
      calculation.calorie_target - nutritionSummary.total_calories,
      0,
    );
  }, [calculation, nutritionSummary]);

  function clearMessages() {
    setError("");
    setSuccess("");
  }

  const savedSex = currentUser?.sex?.trim() || "";

  async function handleCalculate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearMessages();

    const ageValue = Number(age);
    const heightValue = Number(height);
    const weightValue = Number(weight);

    if (!ageValue || !heightValue || !weightValue || !savedSex) {
      setError("Complete your saved fitness profile before calculating targets.");
      return;
    }

    try {
      setCalculating(true);

      const result = await calculateDieticianTargets({
        age: ageValue,
        sex: savedSex,
        height_cm: heightValue,
        weight_kg: weightValue,
        activity_level: activityLevel,
        goal,
      });

      setCalculation(result);
      setSuccess("Nutrition targets calculated successfully.");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to calculate nutrition targets.",
      );
    } finally {
      setCalculating(false);
    }
  }

  async function handleGeneratePlan() {
    clearMessages();

    const ageValue = Number(age);
    const heightValue = Number(height);
    const weightValue = Number(weight);

    if (!ageValue || !heightValue || !weightValue || !savedSex) {
      setError(
        "Complete your saved fitness profile before generating a diet plan.",
      );
      return;
    }

    try {
      setGeneratingPlan(true);

      const plan = await generateDietPlan();

      setDietPlan(plan);
      setSuccess("Personalized diet plan generated from your saved profile.");
      setActiveTab("plan");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to generate the diet plan.",
      );
    } finally {
      setGeneratingPlan(false);
    }
  }

  async function refreshNutrition() {
    try {
      setLoadingNutrition(true);

      const [summary, history] = await Promise.all([
        getNutritionSummary(),
        getNutritionHistory(20, 0),
      ]);

      setNutritionSummary(summary);
      setNutritionHistory(history);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to refresh nutrition data.",
      );
    } finally {
      setLoadingNutrition(false);
    }
  }

  async function handleNutritionSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearMessages();

    if (!foodName.trim()) {
      setError("Enter a food name.");
      return;
    }

    try {
      setLoggingFood(true);

      await createNutritionLog({
        food_name: foodName.trim(),
        quantity: Number(foodQuantity),
        calories: Number(foodCalories),
        protein_g: Number(foodProtein),
        carbohydrates_g: Number(foodCarbs),
        fat_g: Number(foodFat),
      });

      setFoodName("");
      setFoodQuantity("1");
      setFoodCalories("");
      setFoodProtein("");
      setFoodCarbs("");
      setFoodFat("");

      await refreshNutrition();

      setSuccess("Nutrition entry recorded.");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to record nutrition entry.",
      );
    } finally {
      setLoggingFood(false);
    }
  }

  async function handleChatSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearMessages();

    if (!chatMessage.trim()) {
      return;
    }

    try {
      setSendingChat(true);

      const result = await sendDieticianChat({
        message: chatMessage.trim(),
        session_id: chatSessionId,
      });

      setChatSessionId(result.session_id);
      setChatResponse(result.message);
      setChatMessage("");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to reach the Dietician chatbot.",
      );
    } finally {
      setSendingChat(false);
    }
  }

  if (loadingProfile) {
    return (
      <main className="min-h-screen bg-[#050816] text-white">
        <div className="flex min-h-screen items-center justify-center">
          <div className="flex items-center gap-3 text-slate-300">
            <Loader2 className="animate-spin" size={22} />
            Loading your Dietician workspace...
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen overflow-x-hidden bg-[#050816] text-white">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-[10%] top-[-10%] h-[380px] w-[380px] rounded-full bg-cyan-400/[0.06] blur-[120px]" />
        <div className="absolute right-[-5%] top-[20%] h-[460px] w-[460px] rounded-full bg-blue-500/[0.06] blur-[140px]" />
        <div className="absolute bottom-[-10%] left-[30%] h-[420px] w-[420px] rounded-full bg-emerald-400/[0.035] blur-[130px]" />
      </div>

      <div className="relative mx-auto max-w-[1600px] px-5 py-6 sm:px-8 lg:px-10">
        <header className="mb-7 flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <div className="mb-3 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.2em] text-cyan-300">
              <Sparkles size={14} />
              AI Health Intelligence
            </div>

            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
              AI Dietician
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
              Personalized nutrition targets, meal planning, grocery
              intelligence, nutrition tracking, and an AI nutrition coach.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <div
              className={`flex items-center gap-2 rounded-full border px-4 py-2 text-xs ${
                serviceOnline
                  ? "border-emerald-400/20 bg-emerald-400/10 text-emerald-300"
                  : "border-rose-400/20 bg-rose-400/10 text-rose-300"
              }`}
            >
              {serviceOnline ? (
                <CheckCircle2 size={15} />
              ) : (
                <XCircle size={15} />
              )}
              {serviceOnline ? "Dietician Online" : "Service Unavailable"}
            </div>

            <button
              type="button"
              onClick={() => router.push("/dashboard")}
              className="rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-xs text-slate-300 transition hover:border-cyan-400/30 hover:text-white"
            >
              Back to Dashboard
            </button>
          </div>
        </header>

        {error && (
          <div className="mb-5 flex items-start gap-3 rounded-2xl border border-rose-400/20 bg-rose-400/[0.07] px-4 py-3 text-sm text-rose-200">
            <XCircle className="mt-0.5 shrink-0" size={18} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="mb-5 flex items-start gap-3 rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.07] px-4 py-3 text-sm text-emerald-200">
            <CheckCircle2 className="mt-0.5 shrink-0" size={18} />
            <span>{success}</span>
          </div>
        )}

        <section className="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard
            label="Current BMI"
            value={calculation ? calculation.bmi.toFixed(1) : "--"}
            icon={Gauge}
          />

          <StatCard
            label="Daily calorie target"
            value={
              calculation ? formatNumber(calculation.calorie_target) : "--"
            }
            suffix="kcal"
            icon={Flame}
          />

          <StatCard
            label="Protein target"
            value={calculation ? formatNumber(calculation.protein_g) : "--"}
            suffix="g"
            icon={Dumbbell}
          />

          <StatCard
            label="Logged calories"
            value={formatNumber(averageDailyCalories)}
            suffix="kcal"
            icon={Apple}
          />
        </section>

        <nav className="mb-6 overflow-x-auto">
          <div className="flex min-w-max gap-2 rounded-2xl border border-white/10 bg-white/[0.025] p-2">
            {(
                [
              ["overview", "Overview", HeartPulse],
              ["plan", "Diet Plan", ClipboardList],
              ["nutrition", "Nutrition Log", Utensils],
              ["coach", "AI Coach", Bot],
            ]as const
        ).map(([value, label, Icon]) => (
              <button
                key={value}
                type="button"
                onClick={() => setActiveTab(value as TabName)}
                className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm transition ${
                  activeTab === value
                    ? "bg-cyan-400/10 text-cyan-300 shadow-[0_0_30px_rgba(34,211,238,0.06)]"
                    : "text-slate-400 hover:bg-white/[0.04] hover:text-white"
                }`}
              >
                <Icon size={17} />
                {label}
              </button>
            ))}
          </div>
        </nav>

        {activeTab === "overview" && (
          <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
            <section className="rounded-3xl border border-white/10 bg-white/[0.035] p-6 shadow-2xl shadow-cyan-950/10">
              <div className="mb-6 flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                    Personal metrics
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">
                    Nutrition Target Calculator
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">
                    Your saved profile calculates BMI, BMR, calorie targets,
                    and macronutrient targets. Edit details in Profile.
                  </p>
                </div>

                <Calculator
                  size={23}
                  className="text-cyan-300"
                />
              </div>

              <form
                onSubmit={handleCalculate}
                className="grid gap-4 sm:grid-cols-2"
              >
                <label className="space-y-2">
                  <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Age
                  </span>
                  <input
                    value={age}
                    type="number"
                    min="13"
                    max="100"
                    placeholder="Age"
                    disabled
                    className="w-full cursor-not-allowed rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-zinc-400 outline-none"
                  />
                </label>

                <div className="rounded-xl border border-white/10 bg-black/20 px-4 py-3">
                  <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Calorie estimate setting
                  </p>
                  <p className="mt-1 text-sm capitalize text-zinc-300">
                    {savedSex || "Not set"}
                  </p>
                </div>

                <label className="space-y-2">
                  <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Height
                  </span>
                  <div className="relative">
                    <input
                      value={height}
                      type="number"
                      min="100"
                      max="250"
                      step="0.1"
                      placeholder="170"
                      disabled
                      className="w-full cursor-not-allowed rounded-xl border border-white/10 bg-black/20 px-4 py-3 pr-14 text-sm text-zinc-400 outline-none"
                    />
                    <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">
                      cm
                    </span>
                  </div>
                </label>

                <label className="space-y-2">
                  <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Weight
                  </span>
                  <div className="relative">
                    <input
                      value={weight}
                      type="number"
                      min="25"
                      max="300"
                      step="0.1"
                      placeholder="70"
                      disabled
                      className="w-full cursor-not-allowed rounded-xl border border-white/10 bg-black/20 px-4 py-3 pr-14 text-sm text-zinc-400 outline-none"
                    />
                    <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-xs text-slate-500">
                      kg
                    </span>
                  </div>
                </label>

                <label className="space-y-2">
                  <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Activity level
                  </span>
                  <select
                    value={activityLevel}
                    disabled
                    className="w-full cursor-not-allowed rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-zinc-400 outline-none"
                  >
                    {activityOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="space-y-2">
                  <span className="text-xs font-medium uppercase tracking-wide text-slate-500">
                    Fitness goal
                  </span>
                  <select
                    value={goal}
                    disabled
                    className="w-full cursor-not-allowed rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-zinc-400 outline-none"
                  >
                    {goalOptions.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </label>

                <div className="sm:col-span-2 flex flex-wrap gap-3 pt-2">
                  <Link
                    href="/profile"
                    className="inline-flex items-center justify-center rounded-xl border border-white/10 px-5 py-3 text-sm font-medium text-zinc-300 transition hover:bg-white/5"
                  >
                    Edit saved details
                  </Link>
                  <button
                    type="submit"
                    disabled={calculating}
                    className="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {calculating ? (
                      <Loader2 className="animate-spin" size={17} />
                    ) : (
                      <Calculator size={17} />
                    )}
                    {calculating ? "Calculating..." : "Calculate Targets"}
                  </button>

                  <button
                    type="button"
                    onClick={handleGeneratePlan}
                    disabled={generatingPlan}
                    className="inline-flex items-center justify-center gap-2 rounded-xl border border-cyan-400/20 bg-cyan-400/[0.07] px-5 py-3 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-400/10 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {generatingPlan ? (
                      <Loader2 className="animate-spin" size={17} />
                    ) : (
                      <Sparkles size={17} />
                    )}
                    {generatingPlan
                      ? "Generating..."
                      : "Generate Diet Plan"}
                  </button>
                </div>
              </form>
            </section>

            <section className="rounded-3xl border border-white/10 bg-white/[0.035] p-6">
              <div className="mb-6 flex items-start justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                    Your profile
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">
                    Nutrition Intelligence
                  </h2>
                </div>

                <HeartPulse className="text-emerald-300" size={23} />
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between rounded-xl border border-white/7 bg-black/15 px-4 py-3">
                  <span className="text-sm text-slate-400">Name</span>
                  <span className="text-sm font-medium text-white">
                    {currentUser?.full_name.split(" ")[0] || "User"}
                  </span>
                </div>

                <div className="flex items-center justify-between rounded-xl border border-white/7 bg-black/15 px-4 py-3">
                  <span className="text-sm text-slate-400">Activity</span>
                  <span className="text-sm font-medium text-white">
                    {getActivityLabel(activityLevel)}
                  </span>
                </div>

                <div className="flex items-center justify-between rounded-xl border border-white/7 bg-black/15 px-4 py-3">
                  <span className="text-sm text-slate-400">Fitness goal</span>
                  <span className="text-sm font-medium text-white">
                    {getGoalLabel(goal)}
                  </span>
                </div>

                <div className="flex items-center justify-between rounded-xl border border-white/7 bg-black/15 px-4 py-3">
                  <span className="text-sm text-slate-400">
                    Nutrition entries
                  </span>
                  <span className="text-sm font-medium text-cyan-300">
                    {nutritionSummary?.total_entries ?? 0}
                  </span>
                </div>
              </div>

              {calculation && (
                <div className="mt-5 rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.05] p-5">
                  <div className="mb-4 flex items-center justify-between">
                    <span className="text-sm text-slate-400">
                      BMI classification
                    </span>
                    <span
                      className={`rounded-full border px-3 py-1 text-xs ${getBmiTone(
                        calculation.bmi_category,
                      )}`}
                    >
                      {calculation.bmi_category}
                    </span>
                  </div>

                  <div className="text-4xl font-semibold text-white">
                    {calculation.bmi.toFixed(1)}
                  </div>

                  <div className="mt-2 text-sm text-slate-400">
                    BMR:{" "}
                    <span className="text-slate-200">
                      {formatNumber(calculation.bmr)} kcal/day
                    </span>
                  </div>

                  <div className="mt-1 text-sm text-slate-400">
                    Maintenance:{" "}
                    <span className="text-slate-200">
                      {formatNumber(
                        calculation.calorie_target -
                          calculation.calorie_adjustment,
                      )}{" "}
                      kcal/day
                    </span>
                  </div>
                </div>
              )}
            </section>
          </div>
        )}

        {activeTab === "plan" && (
          <div className="space-y-6">
            {!dietPlan ? (
              <section className="rounded-3xl border border-dashed border-white/10 bg-white/[0.025] p-10 text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-400/15 bg-cyan-400/10">
                  <ClipboardList className="text-cyan-300" size={28} />
                </div>

                <h2 className="text-xl font-semibold">
                  Your personalized plan is not generated yet
                </h2>

                <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">
                  Complete your profile details and generate a plan to see
                  your calorie target, meals, macronutrients, and grocery
                  list.
                </p>

                <button
                  type="button"
                  onClick={handleGeneratePlan}
                  disabled={generatingPlan}
                  className="mt-6 inline-flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
                >
                  {generatingPlan ? (
                    <Loader2 className="animate-spin" size={17} />
                  ) : (
                    <Sparkles size={17} />
                  )}
                  Generate Personalized Plan
                </button>
              </section>
            ) : (
              <>
                <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
                  <StatCard
                    label="BMI"
                    value={dietPlan.bmi.toFixed(1)}
                    icon={Gauge}
                  />

                  <StatCard
                    label="BMR"
                    value={formatNumber(dietPlan.bmr)}
                    suffix="kcal"
                    icon={Flame}
                  />

                  <StatCard
                    label="Maintenance"
                    value={formatNumber(dietPlan.maintenance_calories)}
                    suffix="kcal"
                    icon={Target}
                  />

                  <StatCard
                    label="Target"
                    value={formatNumber(dietPlan.target_calories)}
                    suffix="kcal"
                    icon={Sparkles}
                  />

                  <StatCard
                    label="Meals"
                    value={String(dietPlan.meals.length)}
                    icon={Utensils}
                  />
                </section>

                <div className="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
                  <section className="rounded-3xl border border-white/10 bg-white/[0.035] p-6">
                    <div className="mb-6 flex items-center justify-between">
                      <div>
                        <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                          Daily nutrition
                        </p>
                        <h2 className="mt-2 text-xl font-semibold">
                          Personalized Meal Plan
                        </h2>
                      </div>

                      <Apple className="text-emerald-300" size={23} />
                    </div>

                    <div className="space-y-4">
                      {dietPlan.meals.map((meal, index) => (
                        <article
                          key={`${meal.name}-${index}`}
                          className="rounded-2xl border border-white/8 bg-black/15 p-5"
                        >
                          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                            <div className="flex items-start gap-4">
                              <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-emerald-400/15 bg-emerald-400/10">
                                {index === 0 ? (
                                  <Coffee
                                    size={19}
                                    className="text-emerald-300"
                                  />
                                ) : index === dietPlan.meals.length - 1 ? (
                                  <Droplets
                                    size={19}
                                    className="text-emerald-300"
                                  />
                                ) : (
                                  <Utensils
                                    size={19}
                                    className="text-emerald-300"
                                  />
                                )}
                              </div>

                              <div>
                                <div className="text-base font-semibold text-white">
                                  {meal.name}
                                </div>
                                <div className="mt-1 text-xs text-slate-500">
                                  Meal {index + 1}
                                </div>
                              </div>
                            </div>

                            <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
                              <div className="rounded-lg border border-white/7 bg-white/[0.025] px-3 py-2">
                                <div className="text-[10px] uppercase text-slate-500">
                                  Calories
                                </div>
                                <div className="mt-1 text-sm font-semibold text-cyan-300">
                                  {formatNumber(meal.calories)}
                                </div>
                              </div>

                              <div className="rounded-lg border border-white/7 bg-white/[0.025] px-3 py-2">
                                <div className="text-[10px] uppercase text-slate-500">
                                  Protein
                                </div>
                                <div className="mt-1 text-sm font-semibold text-white">
                                  {formatNumber(meal.protein_g)}g
                                </div>
                              </div>

                              <div className="rounded-lg border border-white/7 bg-white/[0.025] px-3 py-2">
                                <div className="text-[10px] uppercase text-slate-500">
                                  Carbs
                                </div>
                                <div className="mt-1 text-sm font-semibold text-white">
                                  {formatNumber(meal.carbohydrates_g)}g
                                </div>
                              </div>

                              <div className="rounded-lg border border-white/7 bg-white/[0.025] px-3 py-2">
                                <div className="text-[10px] uppercase text-slate-500">
                                  Fat
                                </div>
                                <div className="mt-1 text-sm font-semibold text-white">
                                  {formatNumber(meal.fat_g)}g
                                </div>
                              </div>
                            </div>
                          </div>
                        </article>
                      ))}
                    </div>
                  </section>

                  <section className="rounded-3xl border border-white/10 bg-white/[0.035] p-6">
                    <div className="mb-6 flex items-center justify-between">
                      <div>
                        <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                          Smart shopping
                        </p>
                        <h2 className="mt-2 text-xl font-semibold">
                          Grocery List
                        </h2>
                      </div>

                      <ShoppingBasket
                        className="text-cyan-300"
                        size={23}
                      />
                    </div>

                    <div className="space-y-3">
                      {dietPlan.grocery_list.map((item, index) => (
                        <div
                          key={`${item.name}-${index}`}
                          className="flex items-center justify-between gap-4 rounded-xl border border-white/8 bg-black/15 px-4 py-3"
                        >
                          <div className="flex min-w-0 items-center gap-3">
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-cyan-400/10 bg-cyan-400/5">
                              <Package
                                size={16}
                                className="text-cyan-300"
                              />
                            </div>

                            <div className="min-w-0">
                              <div className="truncate text-sm font-medium text-white">
                                {item.name}
                              </div>
                              <div className="mt-0.5 text-xs text-slate-500">
                                {item.category}
                              </div>
                            </div>
                          </div>

                          <div className="shrink-0 text-right">
                            <div className="text-sm font-semibold text-cyan-300">
                              {formatNumber(item.quantity)} {item.unit}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </section>
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === "nutrition" && (
          <div className="grid gap-6 xl:grid-cols-[0.85fr_1.15fr]">
            <section className="rounded-3xl border border-white/10 bg-white/[0.035] p-6">
              <div className="mb-6 flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                    Intake tracker
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">
                    Log Nutrition
                  </h2>
                  <p className="mt-1 text-sm text-slate-400">
                    Save your food intake for personalized nutrition
                    analytics.
                  </p>
                </div>

                <Leaf className="text-emerald-300" size={23} />
              </div>

              <form onSubmit={handleNutritionSubmit} className="space-y-4">
                <label className="block space-y-2">
                  <span className="text-xs uppercase tracking-wide text-slate-500">
                    Food name
                  </span>
                  <input
                    value={foodName}
                    onChange={(event) => setFoodName(event.target.value)}
                    placeholder="Example: Rice"
                    className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400/40"
                  />
                </label>

                <label className="block space-y-2">
                  <span className="text-xs uppercase tracking-wide text-slate-500">
                    Quantity
                  </span>
                  <input
                    value={foodQuantity}
                    onChange={(event) => setFoodQuantity(event.target.value)}
                    type="number"
                    min="0.01"
                    step="0.01"
                    className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none focus:border-cyan-400/40"
                  />
                </label>

                <div className="grid gap-3 sm:grid-cols-2">
                  {[
                    ["Calories", foodCalories, setFoodCalories],
                    ["Protein (g)", foodProtein, setFoodProtein],
                    ["Carbohydrates (g)", foodCarbs, setFoodCarbs],
                    ["Fat (g)", foodFat, setFoodFat],
                  ].map(([label, value, setter]) => (
                    <label
                      key={label as string}
                      className="space-y-2"
                    >
                      <span className="text-xs uppercase tracking-wide text-slate-500">
                        {label as string}
                      </span>
                      <input
                        value={value as string}
                        onChange={(event) =>
                          (setter as (value: string) => void)(
                            event.target.value,
                          )
                        }
                        type="number"
                        min="0"
                        step="0.1"
                        className="w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none focus:border-cyan-400/40"
                      />
                    </label>
                  ))}
                </div>

                <button
                  type="submit"
                  disabled={loggingFood}
                  className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loggingFood ? (
                    <Loader2 className="animate-spin" size={17} />
                  ) : (
                    <CheckCircle2 size={17} />
                  )}
                  {loggingFood ? "Saving..." : "Record Nutrition"}
                </button>
              </form>

              {nutritionSummary && (
                <div className="mt-6 grid grid-cols-2 gap-3">
                  <div className="rounded-xl border border-white/8 bg-black/15 p-4">
                    <div className="text-xs text-slate-500">Entries</div>
                    <div className="mt-1 text-xl font-semibold">
                      {nutritionSummary.total_entries}
                    </div>
                  </div>

                  <div className="rounded-xl border border-white/8 bg-black/15 p-4">
                    <div className="text-xs text-slate-500">Calories</div>
                    <div className="mt-1 text-xl font-semibold text-cyan-300">
                      {formatNumber(nutritionSummary.total_calories)}
                    </div>
                  </div>

                  <div className="rounded-xl border border-white/8 bg-black/15 p-4">
                    <div className="text-xs text-slate-500">Protein</div>
                    <div className="mt-1 text-xl font-semibold">
                      {formatNumber(nutritionSummary.total_protein_g)}g
                    </div>
                  </div>

                  <div className="rounded-xl border border-white/8 bg-black/15 p-4">
                    <div className="text-xs text-slate-500">Carbs</div>
                    <div className="mt-1 text-xl font-semibold">
                      {formatNumber(
                        nutritionSummary.total_carbohydrates_g,
                      )}
                      g
                    </div>
                  </div>
                </div>
              )}
            </section>

            <section className="rounded-3xl border border-white/10 bg-white/[0.035] p-6">
              <div className="mb-6 flex items-center justify-between gap-4">
                <div>
                  <p className="text-xs uppercase tracking-[0.18em] text-slate-500">
                    Nutrition history
                  </p>
                  <h2 className="mt-2 text-xl font-semibold">
                    Recent Intake
                  </h2>
                </div>

                <button
                  type="button"
                  onClick={refreshNutrition}
                  disabled={loadingNutrition}
                  className="flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] text-slate-300 transition hover:text-white disabled:opacity-60"
                  aria-label="Refresh nutrition history"
                >
                  <RefreshCw
                    size={17}
                    className={loadingNutrition ? "animate-spin" : ""}
                  />
                </button>
              </div>

              {nutritionHistory.length === 0 ? (
                <div className="flex min-h-[320px] flex-col items-center justify-center text-center">
                  <History
                    size={34}
                    className="text-slate-600"
                  />
                  <h3 className="mt-4 font-medium text-slate-300">
                    No nutrition entries yet
                  </h3>
                  <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">
                    Your logged meals will appear here once you record them.
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {nutritionHistory.map((entry) => (
                    <div
                      key={entry.id}
                      className="rounded-2xl border border-white/8 bg-black/15 p-4"
                    >
                      <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                        <div>
                          <div className="font-medium text-white">
                            {entry.food_name}
                          </div>
                          <div className="mt-1 text-xs text-slate-500">
                            Quantity: {formatNumber(entry.quantity)}
                          </div>
                          <div className="mt-1 text-xs text-slate-600">
                            {formatDate(entry.consumed_at)}
                          </div>
                        </div>

                        <div className="grid grid-cols-4 gap-2">
                          <div className="rounded-lg border border-white/7 px-3 py-2 text-center">
                            <div className="text-[10px] text-slate-500">
                              KCAL
                            </div>
                            <div className="mt-1 text-xs font-semibold text-cyan-300">
                              {formatNumber(entry.calories)}
                            </div>
                          </div>

                          <div className="rounded-lg border border-white/7 px-3 py-2 text-center">
                            <div className="text-[10px] text-slate-500">
                              PRO
                            </div>
                            <div className="mt-1 text-xs font-semibold text-white">
                              {formatNumber(entry.protein_g)}g
                            </div>
                          </div>

                          <div className="rounded-lg border border-white/7 px-3 py-2 text-center">
                            <div className="text-[10px] text-slate-500">
                              CARB
                            </div>
                            <div className="mt-1 text-xs font-semibold text-white">
                              {formatNumber(
                                entry.carbohydrates_g,
                              )}
                              g
                            </div>
                          </div>

                          <div className="rounded-lg border border-white/7 px-3 py-2 text-center">
                            <div className="text-[10px] text-slate-500">
                              FAT
                            </div>
                            <div className="mt-1 text-xs font-semibold text-white">
                              {formatNumber(entry.fat_g)}g
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {remainingCalories !== null && (
                <div className="mt-5 rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.05] p-5">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-xs uppercase tracking-wide text-slate-500">
                        Remaining target
                      </div>
                      <div className="mt-1 text-2xl font-semibold text-white">
                        {formatNumber(remainingCalories)} kcal
                      </div>
                    </div>

                    <Target className="text-cyan-300" size={26} />
                  </div>
                </div>
              )}
            </section>
          </div>
        )}

        {activeTab === "coach" && (
          <div className="mx-auto max-w-5xl">
            <section className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.035] shadow-2xl shadow-cyan-950/10">
              <div className="border-b border-white/8 bg-gradient-to-r from-cyan-400/[0.07] to-blue-500/[0.04] p-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10">
                    <Bot className="text-cyan-300" size={24} />
                  </div>

                  <div>
                    <div className="text-xs uppercase tracking-[0.18em] text-cyan-300">
                      Conversational AI
                    </div>
                    <h2 className="mt-1 text-xl font-semibold">
                      AI Dietician Coach
                    </h2>
                    <p className="mt-1 text-sm text-slate-400">
                      Ask nutrition questions using your profile and recorded
                      nutrition data.
                    </p>
                  </div>
                </div>
              </div>

              <div className="min-h-[360px] p-6">
                {!chatResponse ? (
                  <div className="flex min-h-[300px] flex-col items-center justify-center text-center">
                    <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-400/15 bg-cyan-400/10">
                      <MessageCircle
                        className="text-cyan-300"
                        size={28}
                      />
                    </div>

                    <h3 className="mt-5 text-lg font-semibold">
                      Start a nutrition conversation
                    </h3>

                    <p className="mt-2 max-w-lg text-sm leading-6 text-slate-500">
                      Ask about calories, macros, your generated plan,
                      nutrition tracking, or general diet-related questions.
                    </p>
                  </div>
                ) : (
                  <div className="flex gap-4">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/10">
                      <Bot size={18} className="text-cyan-300" />
                    </div>

                    <div className="max-w-3xl rounded-2xl rounded-tl-sm border border-white/8 bg-black/15 px-5 py-4">
                      <div className="whitespace-pre-wrap text-sm leading-7 text-slate-200">
                        {chatResponse}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              <div className="border-t border-white/8 p-5">
                <form
                  onSubmit={handleChatSubmit}
                  className="flex flex-col gap-3 sm:flex-row"
                >
                  <input
                    value={chatMessage}
                    onChange={(event) =>
                      setChatMessage(event.target.value)
                    }
                    placeholder="Ask your AI Dietician..."
                    className="min-w-0 flex-1 rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400/40"
                  />

                  <button
                    type="submit"
                    disabled={sendingChat || !chatMessage.trim()}
                    className="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {sendingChat ? (
                      <Loader2 className="animate-spin" size={17} />
                    ) : (
                      <Send size={17} />
                    )}
                    Send
                  </button>
                </form>

                <div className="mt-3 flex items-center gap-2 text-xs text-slate-600">
                  <GlassWater size={14} />
                  AI responses use your available profile and nutrition
                  context.
                </div>
              </div>
            </section>
          </div>
        )}
      </div>
    </main>
  );
}
