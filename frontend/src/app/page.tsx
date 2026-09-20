import { ArrowRight, BrainCircuit, ChartNoAxesCombined, Dumbbell, Salad, ShieldCheck, Sparkles } from "lucide-react";
import Link from "next/link";

import { PublicHeader } from "@/components/public-header";

const features = [
  { icon: Dumbbell, title: "AI Trainer", text: "Use a live camera for squat counting and form cues, or upload a workout video for a detailed report." },
  { icon: Salad, title: "Dietician", text: "Calculate nutrition targets and generate a profile-led diet plan." },
  { icon: BrainCircuit, title: "Fitness companion", text: "Use habit, pose, and gym tools from one place." },
  { icon: ChartNoAxesCombined, title: "Clear progress", text: "See workout, nutrition, and recovery signals together." },
];

export default function Home() {
  return (
    <>
      <PublicHeader />
      <main>
        <section className="mx-auto max-w-7xl px-6 py-16 lg:px-10 lg:py-24"><div className="grid items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]"><div><div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/25 bg-cyan-400/10 px-3 py-1.5 text-sm text-cyan-200"><Sparkles size={15} /> Your connected fitness workspace</div><h1 className="mt-6 max-w-3xl text-4xl font-semibold tracking-tight text-white md:text-6xl">Train smarter. Eat with clarity. Keep moving forward.</h1><p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-400">AI Gym brings workout feedback, diet planning, habits, and fitness insights into one simple experience.</p><div className="mt-8 flex flex-col gap-3 sm:flex-row"><Link href="/register" className="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 font-medium text-black transition hover:bg-cyan-300">Create your account <ArrowRight size={18} /></Link><Link href="/how-it-works" className="inline-flex items-center justify-center rounded-xl border border-white/15 px-5 py-3 font-medium text-white transition hover:border-cyan-400/50 hover:text-cyan-200">See how it works</Link></div></div><div className="rounded-[2rem] border border-cyan-400/20 bg-gradient-to-br from-cyan-400/15 via-[#0e151d] to-[#090b0f] p-7 shadow-[0_0_60px_rgba(34,211,238,0.08)]"><p className="text-xs font-medium uppercase tracking-[0.2em] text-cyan-200">AI Gym overview</p><h2 className="mt-4 text-2xl font-semibold text-white">Your fitness system, connected.</h2><div className="mt-7 space-y-4">{["Personal training space", "Diet targets that use your profile", "Simple progress visibility"].map((item) => <div key={item} className="flex items-center gap-3 rounded-2xl border border-white/10 bg-black/20 p-4 text-zinc-200"><ShieldCheck className="text-cyan-300" size={20} />{item}</div>)}</div></div></div></section>

        <section className="border-y border-white/10 bg-white/[0.02]"><div className="mx-auto max-w-7xl px-6 py-16 lg:px-10"><p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Explore the workspace</p><h2 className="mt-4 max-w-2xl text-3xl font-semibold tracking-tight text-white md:text-4xl">Everything you need to build a more intentional routine.</h2><div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">{features.map((feature) => { const Icon = feature.icon; return <article key={feature.title} className="rounded-3xl border border-white/10 bg-[#0b0e13] p-6"><div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/10 text-cyan-300"><Icon size={22} /></div><h3 className="mt-5 text-lg font-semibold text-white">{feature.title}</h3><p className="mt-3 text-sm leading-6 text-zinc-400">{feature.text}</p></article>; })}</div></div></section>

        <section className="mx-auto max-w-7xl px-6 py-16 lg:px-10"><div className="grid gap-10 lg:grid-cols-2"><div><p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">Personalized diet planning</p><h2 className="mt-4 text-3xl font-semibold tracking-tight text-white md:text-4xl">Enter a few details. Get a plan built around your goal.</h2><p className="mt-5 max-w-xl leading-7 text-zinc-400">Your saved profile helps the Dietician calculate targets and create a plan with useful context—not generic advice.</p><Link href="/diet-plans" className="mt-6 inline-flex items-center gap-2 text-cyan-300 transition hover:text-cyan-100">View diet plans <ArrowRight size={17} /></Link></div><div className="rounded-3xl border border-white/10 bg-[#0b1118] p-7"><p className="text-xs uppercase tracking-[0.18em] text-zinc-500">Quick setup</p><ol className="mt-6 space-y-5">{["Create your account", "Save your fitness profile", "Generate your personalized diet plan"].map((item, index) => <li key={item} className="flex gap-4"><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cyan-400 font-semibold text-black">{index + 1}</span><span className="pt-1 text-zinc-200">{item}</span></li>)}</ol></div></div></section>

        <section className="border-t border-white/10 bg-cyan-400/10"><div className="mx-auto flex max-w-7xl flex-col items-start justify-between gap-6 px-6 py-14 lg:flex-row lg:items-center lg:px-10"><div><h2 className="text-3xl font-semibold text-white">Your next fitness step starts here.</h2><p className="mt-3 text-zinc-300">Create an account to unlock the complete workspace.</p></div><Link href="/register" className="inline-flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 font-medium text-black transition hover:bg-cyan-300">Create account <ArrowRight size={18} /></Link></div></section>
      </main>
    </>
  );
}
