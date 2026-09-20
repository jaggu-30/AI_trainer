"use client";

import { FormEvent, useState } from "react";
import {
  ArrowRight,
  Dumbbell,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import {
  ApiError,
  getCurrentUser,
  login,
  logout,
} from "@/lib/api";
import { hasCompletedFitnessSetup } from "@/lib/fitness-profile";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] =
    useState(false);
  const [isSubmitting, setIsSubmitting] =
    useState(false);
  const [errorMessage, setErrorMessage] =
    useState("");

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setErrorMessage("");
    setIsSubmitting(true);

    try {
      await login({
        username: email.trim(),
        password,
      });

      const user = await getCurrentUser();

      if (user.is_admin) {
        logout();
        setErrorMessage(
          "This is an administrator account. Use the separate admin sign-in page.",
        );
        return;
      }

      router.replace(
        hasCompletedFitnessSetup(user) ? "/dashboard" : "/onboarding",
      );
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError) {
        setErrorMessage(error.detail);
      } else {
        setErrorMessage(
          "Unable to sign in right now. Please try again.",
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#06070a] text-white">
      <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-5 py-10">
        <div className="pointer-events-none absolute left-1/2 top-[-180px] h-[480px] w-[480px] -translate-x-1/2 rounded-full bg-cyan-400/10 blur-3xl" />

        <div className="pointer-events-none absolute bottom-[-220px] left-[-120px] h-[420px] w-[420px] rounded-full bg-cyan-500/5 blur-3xl" />

        <section className="relative grid w-full max-w-5xl overflow-hidden rounded-[2rem] border border-white/10 bg-[#0a0c10]/95 shadow-[0_35px_100px_rgba(0,0,0,0.5)] lg:grid-cols-[1.05fr_0.95fr]">
          <div className="hidden border-r border-white/10 bg-gradient-to-br from-cyan-400/[0.08] via-[#0b0e14] to-[#080a0d] p-10 lg:flex lg:flex-col lg:justify-between">
            <div>
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400 text-black shadow-[0_0_35px_rgba(34,211,238,0.3)]">
                  <Sparkles size={21} />
                </div>

                <div>
                  <p className="text-sm font-semibold tracking-[0.18em] text-cyan-300">
                    AI GYM
                  </p>

                  <p className="text-xs text-zinc-500">
                    Fitness Intelligence
                  </p>
                </div>
              </div>

              <div className="mt-20 max-w-md">
                <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-300/15 bg-cyan-300/5 px-3 py-1.5 text-xs font-medium text-cyan-200">
                  <ShieldCheck size={14} />
                  Secure fitness workspace
                </div>

                <h1 className="text-4xl font-semibold leading-tight tracking-tight">
                  Your intelligent
                  <span className="text-cyan-300">
                    {" "}
                    fitness system
                  </span>{" "}
                  starts here.
                </h1>

                <p className="mt-5 text-sm leading-7 text-zinc-500">
                  Connect your AI Trainer, Dietician, Habit
                  AI, Gym Buddy, Pose Analysis, Smart Gym, and
                  analytics inside one personalized platform.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                <Dumbbell
                  size={18}
                  className="text-cyan-300"
                />

                <p className="mt-3 text-sm font-medium">
                  AI Trainer
                </p>

                <p className="mt-1 text-xs text-zinc-600">
                  Performance intelligence
                </p>
              </div>

              <div className="rounded-2xl border border-white/5 bg-white/[0.025] p-4">
                <ShieldCheck
                  size={18}
                  className="text-cyan-300"
                />

                <p className="mt-3 text-sm font-medium">
                  Secure Access
                </p>

                <p className="mt-1 text-xs text-zinc-600">
                  Protected account session
                </p>
              </div>
            </div>
          </div>

          <div className="p-6 sm:p-8 md:p-10">
            <div className="mx-auto max-w-md">
              <div className="flex items-center gap-3 lg:hidden">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-400 text-black">
                  <Sparkles size={19} />
                </div>

                <div>
                  <p className="text-sm font-semibold tracking-[0.16em] text-cyan-300">
                    AI GYM
                  </p>

                  <p className="text-xs text-zinc-600">
                    Fitness Intelligence
                  </p>
                </div>
              </div>

              <div className="mt-8 lg:mt-0">
                <p className="text-xs font-medium uppercase tracking-[0.2em] text-zinc-600">
                  User sign in
                </p>

                <h2 className="mt-3 text-3xl font-semibold tracking-tight">
                  Sign in to your fitness workspace
                </h2>

                <p className="mt-3 text-sm leading-6 text-zinc-500">
                  Enter your account credentials to continue.
                </p>
              </div>

              {errorMessage && (
                <div className="mt-6 rounded-2xl border border-red-400/15 bg-red-400/5 px-4 py-3 text-sm leading-6 text-red-300">
                  {errorMessage}
                </div>
              )}

              <form
                onSubmit={handleSubmit}
                className="mt-8 space-y-5"
              >
                <div>
                  <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-medium text-zinc-300"
                  >
                    Email address
                  </label>

                  <div className="relative">
                    <Mail
                      size={17}
                      className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600"
                    />

                    <input
                      id="email"
                      name="email"
                      type="email"
                      autoComplete="email"
                      required
                      value={email}
                      onChange={(event) =>
                        setEmail(event.target.value)
                      }
                      placeholder="you@example.com"
                      className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-cyan-300/40 focus:bg-white/[0.04] focus:ring-2 focus:ring-cyan-300/10"
                    />
                  </div>
                </div>

                <div>
                  <label
                    htmlFor="password"
                    className="mb-2 block text-sm font-medium text-zinc-300"
                  >
                    Password
                  </label>

                  <div className="relative">
                    <LockKeyhole
                      size={17}
                      className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600"
                    />

                    <input
                      id="password"
                      name="password"
                      type={
                        showPassword
                          ? "text"
                          : "password"
                      }
                      autoComplete="current-password"
                      required
                      value={password}
                      onChange={(event) =>
                        setPassword(event.target.value)
                      }
                      placeholder="Enter your password"
                      className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] pl-11 pr-12 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-cyan-300/40 focus:bg-white/[0.04] focus:ring-2 focus:ring-cyan-300/10"
                    />

                    <button
                      type="button"
                      aria-label={
                        showPassword
                          ? "Hide password"
                          : "Show password"
                      }
                      onClick={() =>
                        setShowPassword(
                          (visible) => !visible,
                        )
                      }
                      className="absolute right-3 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-lg text-zinc-600 transition hover:bg-white/5 hover:text-zinc-300"
                    >
                      {showPassword ? (
                        <EyeOff size={17} />
                      ) : (
                        <Eye size={17} />
                      )}
                    </button>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="group flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {isSubmitting
                    ? "Signing in..."
                    : "Sign in"}

                  {!isSubmitting && (
                    <ArrowRight
                      size={17}
                      className="transition-transform group-hover:translate-x-0.5"
                    />
                  )}
                </button>
              </form>

              <div className="mt-6 text-center text-sm text-zinc-500">
                New to AI Gym?{" "}
                <Link
                  href="/register"
                  className="font-medium text-cyan-300 transition hover:text-cyan-200"
                >
                  Create an account
                </Link>
              </div>

              <div className="mt-8 flex items-start gap-3 rounded-2xl border border-white/5 bg-white/[0.02] p-4">
                <ShieldCheck
                  size={18}
                  className="mt-0.5 shrink-0 text-emerald-300"
                />

                <p className="text-xs leading-5 text-zinc-600">
                  Authentication is validated by the backend.
                  Administrative privileges are enforced
                  server-side.
                </p>
              </div>

              <Link
                href="/admin/login"
                className="mt-5 flex items-center justify-center rounded-xl border border-white/10 px-4 py-3 text-sm font-medium text-zinc-400 transition hover:border-cyan-300/30 hover:bg-white/[0.03] hover:text-cyan-200"
              >
                Administrator sign in
              </Link>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
