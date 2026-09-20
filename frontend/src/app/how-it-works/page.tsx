import { ArrowRight, BrainCircuit, Camera, ChartNoAxesCombined, Salad } from "lucide-react";
import Link from "next/link";

import { PublicHeader } from "@/components/public-header";

const steps = [
  { icon: BrainCircuit, title: "Create your fitness profile", text: "Tell us your goal, activity level, height, and weight so the workspace can adapt to you." },
  { icon: Camera, title: "Train and check your form", text: "Open the Live AI Trainer for real-time squat counting and form cues, or upload a recording for a full report." },
  { icon: Salad, title: "Plan food with context", text: "Calculate nutrition targets and generate a diet plan from the profile you saved." },
  { icon: ChartNoAxesCombined, title: "Review your progress", text: "Use one simple dashboard for workout, nutrition, habit, and smart-gym signals." },
];

export default function HowItWorksPage() {
  return (
    <>
      <PublicHeader />
      <main className="mx-auto max-w-7xl px-6 py-16 lg:px-10 lg:py-24">
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-cyan-300">How it works</p>
        <h1 className="mt-4 max-w-3xl text-4xl font-semibold tracking-tight text-white md:text-6xl">One calm workspace for better fitness decisions.</h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-zinc-400">AI Gym connects your training, nutrition, and daily momentum without making the experience complicated.</p>

        <section className="mt-14 grid gap-5 md:grid-cols-2" aria-label="How AI Gym works">
          {steps.map((step, index) => {
            const Icon = step.icon;
            return <article key={step.title} className="rounded-3xl border border-white/10 bg-white/[0.025] p-7"><div className="flex items-center justify-between"><div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-400/10 text-cyan-300"><Icon size={23} /></div><span className="text-sm font-medium text-zinc-600">0{index + 1}</span></div><h2 className="mt-6 text-xl font-semibold text-white">{step.title}</h2><p className="mt-3 leading-7 text-zinc-400">{step.text}</p></article>;
          })}
        </section>

        <section className="mt-16 flex flex-col justify-between gap-6 rounded-3xl border border-cyan-400/20 bg-cyan-400/10 p-8 sm:flex-row sm:items-center"><div><h2 className="text-2xl font-semibold text-white">Ready to make your plan personal?</h2><p className="mt-2 text-zinc-300">Create a free account to use the fitness workspace.</p></div><Link href="/register" className="inline-flex items-center justify-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 font-medium text-black transition hover:bg-cyan-300">Create account <ArrowRight size={18} /></Link></section>
      </main>
    </>
  );
}
