"use client";

import { FormEvent, useState } from "react";
import {
  ArrowRight,
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

export default function AdminLoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setErrorMessage("");
    setIsSubmitting(true);

    try {
      await login({
        username: email.trim(),
        password,
      });

      const user = await getCurrentUser();

      if (!user.is_admin) {
        logout();
        setErrorMessage(
          "This account does not have administrator access. Use the user sign-in page.",
        );
        return;
      }

      router.replace("/admin");
      router.refresh();
    } catch (error) {
      if (error instanceof ApiError) {
        logout();
        setErrorMessage(error.detail);
      } else {
        setErrorMessage("Unable to sign in right now. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-[#06070a] px-5 py-10 text-white">
      <div className="relative mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-xl items-center">
        <div className="pointer-events-none absolute left-1/2 top-1/2 h-80 w-80 -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-400/10 blur-3xl" />

        <section className="relative w-full rounded-[2rem] border border-cyan-300/15 bg-[#0a0c10] p-6 shadow-[0_35px_100px_rgba(0,0,0,0.45)] sm:p-9">
          <Link href="/login" className="inline-flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400 text-black">
              <Sparkles size={21} />
            </div>
            <div>
              <p className="text-sm font-semibold tracking-[0.18em] text-cyan-300">
                AI GYM
              </p>
              <p className="text-xs text-zinc-500">Fitness Intelligence</p>
            </div>
          </Link>

          <div className="mt-9 flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-300">
              <ShieldCheck size={22} />
            </div>
            <div>
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-cyan-300">
                Restricted access
              </p>
              <h1 className="mt-2 text-3xl font-semibold tracking-tight">
                Administrator sign in
              </h1>
              <p className="mt-3 text-sm leading-6 text-zinc-500">
                Use an account assigned administrator privileges by the system owner.
              </p>
            </div>
          </div>

          {errorMessage && (
            <div className="mt-6 rounded-2xl border border-red-400/15 bg-red-400/5 px-4 py-3 text-sm leading-6 text-red-300">
              {errorMessage}
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            <div>
              <label htmlFor="admin-email" className="mb-2 block text-sm font-medium text-zinc-300">
                Administrator email
              </label>
              <div className="relative">
                <Mail size={17} className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600" />
                <input
                  id="admin-email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="admin@example.com"
                  className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                />
              </div>
            </div>

            <div>
              <label htmlFor="admin-password" className="mb-2 block text-sm font-medium text-zinc-300">
                Password
              </label>
              <div className="relative">
                <LockKeyhole size={17} className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600" />
                <input
                  id="admin-password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Enter your password"
                  className="h-12 w-full rounded-xl border border-white/10 bg-white/[0.025] pl-11 pr-12 text-sm text-white outline-none transition placeholder:text-zinc-700 focus:border-cyan-300/40 focus:ring-2 focus:ring-cyan-300/10"
                />
                <button
                  type="button"
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  onClick={() => setShowPassword((visible) => !visible)}
                  className="absolute right-3 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-lg text-zinc-600 transition hover:bg-white/5 hover:text-zinc-300"
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 text-sm font-semibold text-black transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isSubmitting ? "Signing in..." : "Open admin workspace"}
              {!isSubmitting && <ArrowRight size={17} />}
            </button>
          </form>

          <p className="mt-7 text-center text-sm text-zinc-500">
            Need a user account?{" "}
            <Link href="/login" className="font-medium text-cyan-300 transition hover:text-cyan-200">
              User sign in
            </Link>
          </p>
        </section>
      </div>
    </main>
  );
}
