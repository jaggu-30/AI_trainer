import { Code2, Mail, Phone, Sparkles } from "lucide-react";
import Link from "next/link";

import { PublicHeader } from "@/components/public-header";

export default function AboutPage() {
  return (
    <>
      <PublicHeader />
      <main className="mx-auto max-w-5xl px-6 py-16 lg:px-10 lg:py-24">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">About the developer</p>
        <div className="mt-5 rounded-[2rem] border border-white/10 bg-gradient-to-br from-cyan-400/10 via-[#0d121a] to-[#0a0c10] p-8 md:p-12">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-cyan-400 text-black"><Code2 size={28} /></div>
          <h1 className="mt-7 text-4xl font-semibold tracking-tight text-white md:text-6xl">Jagadeesh Nayak V</h1>
          <p className="mt-4 text-xl text-cyan-200">Developer of AI Gym &amp; Fitness Assistant</p>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-400">I built this project to bring training guidance, nutrition planning, and fitness progress into one focused digital workspace.</p>
        </div>

        <section className="mt-8 grid gap-5 md:grid-cols-2" aria-label="Developer contact details">
          <a href="mailto:jagadeeshnayakv@gmail.com" className="rounded-3xl border border-white/10 bg-white/[0.025] p-7 transition hover:border-cyan-400/40"><Mail className="text-cyan-300" size={23} /><p className="mt-5 text-sm uppercase tracking-[0.16em] text-zinc-500">Email</p><p className="mt-2 break-all text-lg font-medium text-white">jagadeeshnayakv@gmail.com</p></a>
          <a href="tel:+918147011107" className="rounded-3xl border border-white/10 bg-white/[0.025] p-7 transition hover:border-cyan-400/40"><Phone className="text-cyan-300" size={23} /><p className="mt-5 text-sm uppercase tracking-[0.16em] text-zinc-500">Phone</p><p className="mt-2 text-lg font-medium text-white">8147011107</p></a>
        </section>

        <section className="mt-8 rounded-3xl border border-white/10 bg-white/[0.025] p-8"><Sparkles className="text-cyan-300" size={24} /><h2 className="mt-5 text-2xl font-semibold text-white">Start your AI Gym journey</h2><p className="mt-3 leading-7 text-zinc-400">Create an account to access personalized training, diet planning, fitness analytics, and more.</p><Link href="/register" className="mt-6 inline-flex rounded-xl bg-cyan-400 px-5 py-3 font-medium text-black transition hover:bg-cyan-300">Create account</Link></section>
      </main>
    </>
  );
}
