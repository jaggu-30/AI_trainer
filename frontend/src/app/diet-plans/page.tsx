import { ArrowRight, Check, Salad, Sparkles } from "lucide-react";
import Link from "next/link";

import { PublicHeader } from "@/components/public-header";

const plans = [
  { title: "Balanced routine", description: "A steady framework for people building consistent food habits.", points: ["Daily calorie target", "Protein, carbohydrate, and fat guidance", "Simple meal structure"] },
  { title: "Strength & weight gain", description: "A profile-led starting point for supporting progressive training.", points: ["Energy-surplus target", "Protein focus", "Easy nutrition logging"] },
  { title: "Weight-management focus", description: "A practical starting point for a sustainable, mindful routine.", points: ["Personal calorie estimate", "Goal-aware macros", "Progress view in one dashboard"] },
];

export default function DietPlansPage() {
  return (
    <>
      <PublicHeader />
      <main className="mx-auto max-w-7xl px-6 py-16 lg:px-10 lg:py-24">
        <div className="max-w-3xl"><div className="inline-flex items-center gap-2 rounded-full border border-cyan-400/25 bg-cyan-400/10 px-3 py-1 text-sm text-cyan-200"><Salad size={15} /> Nutrition intelligence</div><h1 className="mt-5 text-4xl font-semibold tracking-tight text-white md:text-6xl">Diet planning that starts with your real profile.</h1><p className="mt-6 text-lg leading-8 text-zinc-400">Sign in, add your basic fitness details, and let the Dietician workspace calculate targets before generating a personalized plan.</p></div>
        <section className="mt-14 grid gap-5 lg:grid-cols-3" aria-label="Diet plan previews">{plans.map((plan, index) => <article key={plan.title} className={`rounded-3xl border p-7 ${index === 1 ? "border-cyan-400/40 bg-cyan-400/[0.08]" : "border-white/10 bg-white/[0.025]"}`}>{index === 1 && <p className="inline-flex items-center gap-2 rounded-full bg-cyan-400 px-3 py-1 text-xs font-medium text-black"><Sparkles size={13} /> Popular focus</p>}<h2 className="mt-5 text-2xl font-semibold text-white">{plan.title}</h2><p className="mt-3 min-h-14 leading-7 text-zinc-400">{plan.description}</p><ul className="mt-6 space-y-3 text-sm text-zinc-300">{plan.points.map((point) => <li key={point} className="flex gap-3"><Check size={17} className="mt-0.5 shrink-0 text-cyan-300" />{point}</li>)}</ul></article>)}</section>
        <section className="mt-10 rounded-3xl border border-white/10 bg-[#0b1118] p-8"><h2 className="text-2xl font-semibold text-white">Your plan is ready after a quick profile setup.</h2><p className="mt-3 max-w-2xl leading-7 text-zinc-400">Enter your age, height, weight, activity level, and goal. Those values stay with your account and are used when you request your diet plan.</p><Link href="/register" className="mt-6 inline-flex items-center gap-2 rounded-xl bg-cyan-400 px-5 py-3 font-medium text-black transition hover:bg-cyan-300">Create an account <ArrowRight size={18} /></Link></section>
      </main>
    </>
  );
}
