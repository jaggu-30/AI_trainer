import { Mail, Phone, Sparkles } from "lucide-react";
import Link from "next/link";

export function SiteFooter() {
  return (
    <footer className="border-t border-white/10 bg-[#080a0e]">
      <div className="mx-auto flex max-w-7xl flex-col gap-5 px-6 py-8 text-sm text-zinc-400 sm:flex-row sm:items-center sm:justify-between lg:px-10">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-400 text-black">
            <Sparkles size={17} />
          </div>
          <div>
            <p className="font-medium text-white">AI Gym &amp; Fitness Assistant</p>
            <p className="text-xs text-zinc-500">Built by Jagadeesh Nayak V</p>
          </div>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-5">
          <a
            href="mailto:jagadeeshnayakv@gmail.com"
            className="inline-flex items-center gap-2 transition hover:text-cyan-300"
          >
            <Mail size={15} />
            jagadeeshnayakv@gmail.com
          </a>
          <a
            href="tel:+918147011107"
            className="inline-flex items-center gap-2 transition hover:text-cyan-300"
          >
            <Phone size={15} />
            8147011107
          </a>
          <Link href="/about" className="transition hover:text-cyan-300">
            About the developer
          </Link>
        </div>
      </div>
    </footer>
  );
}
