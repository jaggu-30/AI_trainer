"use client";

import { Mail, Menu, Phone, Sparkles, X } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

const links = [
  ["/", "Home"],
  ["/how-it-works", "How it works"],
  ["/diet-plans", "Diet plans"],
  ["/about", "About"],
] as const;

export function PublicHeader() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="border-b border-white/10 bg-[#080a0e]/95 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-6 py-4 lg:px-10">
        <Link href="/" className="flex shrink-0 items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-cyan-400 text-black shadow-[0_0_30px_rgba(34,211,238,0.25)]">
            <Sparkles size={19} />
          </div>
          <div>
            <p className="text-sm font-semibold tracking-[0.16em] text-cyan-300">AI GYM</p>
            <p className="text-[11px] text-zinc-500">Fitness Intelligence</p>
          </div>
        </Link>

        <nav className="hidden items-center gap-6 text-sm text-zinc-400 md:flex" aria-label="Public navigation">
          {links.map(([href, label]) => (
            <Link key={href} href={href} className="transition hover:text-cyan-300">
              {label}
            </Link>
          ))}
        </nav>

        <div className="hidden items-center gap-4 xl:flex">
          <a href="mailto:jagadeeshnayakv@gmail.com" className="inline-flex items-center gap-2 text-xs text-zinc-400 transition hover:text-cyan-300">
            <Mail size={14} /> jagadeeshnayakv@gmail.com
          </a>
          <a href="tel:+918147011107" className="inline-flex items-center gap-2 text-xs text-zinc-400 transition hover:text-cyan-300">
            <Phone size={14} /> 8147011107
          </a>
        </div>

        <div className="flex items-center gap-2">
          <Link href="/login" className="hidden rounded-xl px-4 py-2 text-sm text-zinc-300 transition hover:bg-white/5 hover:text-white sm:inline-flex">Sign in</Link>
          <Link href="/register" className="rounded-xl bg-cyan-400 px-4 py-2 text-sm font-medium text-black transition hover:bg-cyan-300">Create account</Link>
          <button
            type="button"
            aria-label={menuOpen ? "Close menu" : "Open menu"}
            aria-expanded={menuOpen}
            onClick={() => setMenuOpen((open) => !open)}
            className="rounded-lg p-2 text-zinc-400 transition hover:bg-white/5 hover:text-white md:hidden"
          >
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="border-t border-white/10 px-6 py-5 md:hidden">
          <nav className="grid gap-1" aria-label="Mobile public navigation">
            {links.map(([href, label]) => (
              <Link
                key={href}
                href={href}
                onClick={() => setMenuOpen(false)}
                className="rounded-xl px-3 py-2.5 text-sm text-zinc-300 transition hover:bg-white/5 hover:text-cyan-200"
              >
                {label}
              </Link>
            ))}
          </nav>
          <div className="mt-4 grid gap-2 border-t border-white/10 pt-4 text-sm text-zinc-400">
            <a href="mailto:jagadeeshnayakv@gmail.com" className="inline-flex items-center gap-2"><Mail size={15} /> jagadeeshnayakv@gmail.com</a>
            <a href="tel:+918147011107" className="inline-flex items-center gap-2"><Phone size={15} /> 8147011107</a>
          </div>
        </div>
      )}
    </header>
  );
}
