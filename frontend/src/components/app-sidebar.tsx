"use client";

import {
  Activity,
  Camera,
  Dumbbell,
  HeartPulse,
  LogOut,
  Mail,
  MapPin,
  MessageCircle,
  Phone,
  Salad,
  ShieldCheck,
  Sparkles,
  Target,
  UserRound,
  Watch,
} from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getAccessToken } from "@/lib/auth";
import { getCurrentUser, logout } from "@/lib/api";

const navigation = [
  ["/dashboard", "Dashboard", Activity],
  ["/my-plan", "My Plan", Sparkles],
  ["/trainer", "AI Trainer", Dumbbell],
  ["/live-trainer", "Live AI Trainer", Camera],
  ["/dietician", "Dietician", Salad],
  ["/gym-buddy", "Gym Buddy", MessageCircle],
  ["/habits", "Habit AI", Target],
  ["/pose-analysis", "Pose Analysis", Activity],
  ["/smart-gym", "Smart Gym", Watch],
  ["/planner", "Fitness Planner", MapPin],
  ["/analytics", "Analytics", HeartPulse],
  ["/profile", "Profile", UserRound],
] as const;

export function AppSidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadAccess() {
      if (!getAccessToken()) {
        return;
      }

      try {
        const user = await getCurrentUser();

        if (!cancelled) {
          setIsAdmin(user.is_admin);
        }
      } catch {
        if (!cancelled) {
          setIsAdmin(false);
        }
      }
    }

    void loadAccess();

    return () => {
      cancelled = true;
    };
  }, [pathname]);

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  return (
    <aside className="hidden h-screen w-72 shrink-0 flex-col border-r border-white/10 bg-[#0a0c10] lg:sticky lg:top-0 lg:flex">
      <div className="border-b border-white/10 px-6 py-6">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400 text-black shadow-[0_0_35px_rgba(34,211,238,0.3)]">
            <Sparkles size={21} />
          </div>

          <div>
            <p className="text-sm font-semibold tracking-[0.18em] text-cyan-300">
              AI GYM
            </p>
            <p className="text-xs text-zinc-500">Fitness Intelligence</p>
          </div>
        </Link>
      </div>

      <nav className="flex-1 overflow-y-auto px-4 py-6" aria-label="Main navigation">
        <p className="px-3 pb-3 text-[11px] font-medium uppercase tracking-[0.2em] text-zinc-600">
          Workspace
        </p>

        <div className="space-y-1">
          {navigation.map(([href, label, Icon]) => {
            const active = pathname === href;

            return (
              <Link
                key={href}
                href={href}
                className={`group flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition ${
                  active
                    ? "bg-cyan-400 font-medium text-black"
                    : "text-zinc-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <Icon
                  size={18}
                  className={
                    active
                      ? "text-black"
                      : "text-zinc-600 group-hover:text-cyan-300"
                  }
                />
                {label}
              </Link>
            );
          })}

          {isAdmin && (
            <>
              <p className="px-3 pb-2 pt-6 text-[11px] font-medium uppercase tracking-[0.2em] text-zinc-600">
                Administration
              </p>
              <Link
                href="/admin"
                className={`group flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition ${
                  pathname === "/admin"
                    ? "bg-cyan-400 font-medium text-black"
                    : "text-zinc-400 hover:bg-white/5 hover:text-white"
                }`}
              >
                <ShieldCheck
                  size={18}
                  className={
                    pathname === "/admin"
                      ? "text-black"
                      : "text-zinc-600 group-hover:text-cyan-300"
                  }
                />
                Admin workspace
              </Link>
            </>
          )}
        </div>
      </nav>

      <div className="border-t border-white/10 px-6 py-4">
        <p className="text-[10px] font-medium uppercase tracking-[0.18em] text-zinc-600">
          Contact
        </p>
        <a
          href="mailto:jagadeeshnayakv@gmail.com"
          className="mt-2 flex items-center gap-2 text-xs text-zinc-400 transition hover:text-cyan-300"
        >
          <Mail size={14} className="shrink-0" />
          jagadeeshnayakv@gmail.com
        </a>
        <a
          href="tel:+918147011107"
          className="mt-2 flex items-center gap-2 text-xs text-zinc-400 transition hover:text-cyan-300"
        >
          <Phone size={14} className="shrink-0" />
          8147011107
        </a>
      </div>

      <div className="border-t border-white/10 p-4">
        <button
          type="button"
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm text-zinc-500 transition hover:bg-white/5 hover:text-red-300"
        >
          <LogOut size={18} />
          Sign out
        </button>
      </div>
    </aside>
  );
}
