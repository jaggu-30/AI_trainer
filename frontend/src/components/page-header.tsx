import { ArrowLeft, type LucideIcon } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";

type PageHeaderProps = {
  eyebrow: string;
  title: string;
  description: string;
  icon: LucideIcon;
  action?: ReactNode;
};

export function PageHeader({
  eyebrow,
  title,
  description,
  icon: Icon,
  action,
}: PageHeaderProps) {
  return (
    <header className="flex flex-col gap-5 border-b border-white/10 pb-7 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <Link
          href="/dashboard"
          className="inline-flex items-center gap-2 text-xs text-zinc-500 transition hover:text-cyan-300"
        >
          <ArrowLeft size={14} />
          Back to dashboard
        </Link>

        <div className="mt-5 flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-cyan-400 text-black shadow-[0_0_32px_rgba(34,211,238,0.22)]">
            <Icon size={22} />
          </div>

          <div>
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-300">
              {eyebrow}
            </p>

            <h1 className="mt-1 text-2xl font-semibold tracking-tight md:text-3xl">
              {title}
            </h1>
          </div>
        </div>

        <p className="mt-4 max-w-2xl text-sm leading-6 text-zinc-500">
          {description}
        </p>
      </div>

      {action}
    </header>
  );
}
