type SquatMovementGuideProps = {
  compact?: boolean;
};

export function SquatMovementGuide({
  compact = false,
}: SquatMovementGuideProps) {
  return (
    <div className={compact ? "w-full max-w-sm" : "rounded-3xl border border-cyan-300/15 bg-cyan-300/[0.04] p-5"}>
      {!compact && (
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.16em] text-cyan-200/70">Movement guide</p>
          <h2 className="mt-1 text-lg font-semibold">Copy the squat position</h2>
        </div>
      )}

      <div className="mt-3 rounded-2xl border border-white/10 bg-[#071016] px-3 py-2">
        <svg
          viewBox="0 0 360 210"
          role="img"
          aria-label="Animated guide showing a person moving through a controlled squat"
          className="h-auto w-full"
        >
          <defs>
            <linearGradient id="guideGlow" x1="0" y1="0" x2="1" y2="1">
              <stop stopColor="#67e8f9" />
              <stop offset="1" stopColor="#22d3ee" />
            </linearGradient>
          </defs>
          <path d="M35 176H325" stroke="#334155" strokeWidth="2" strokeDasharray="5 5" />
          <text x="30" y="198" fill="#94a3b8" fontSize="12">Start</text>
          <text x="264" y="198" fill="#94a3b8" fontSize="12">Squat depth</text>

          <g transform="translate(84 22)" stroke="url(#guideGlow)" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" fill="none">
            <animateTransform attributeName="transform" type="translate" values="84 22;84 44;84 22" dur="2.8s" repeatCount="indefinite" />
            <circle cx="42" cy="21" r="15" fill="#67e8f9" stroke="none" />
            <path d="M42 41L42 92" />
            <path d="M42 55L8 76M42 55L76 71" />
            <path d="M42 91L21 139L4 154M42 91L67 137L92 154" />
          </g>

          <g transform="translate(235 54)" stroke="url(#guideGlow)" strokeWidth="9" strokeLinecap="round" strokeLinejoin="round" fill="none">
            <animateTransform attributeName="transform" type="translate" values="235 54;235 30;235 54" dur="2.8s" repeatCount="indefinite" />
            <circle cx="42" cy="21" r="15" fill="#67e8f9" stroke="none" />
            <path d="M42 41L30 84" />
            <path d="M37 56L4 75M37 56L72 73" />
            <path d="M30 84L-2 105L10 151M30 84L66 105L83 151" />
          </g>

          <path d="M205 117H178" stroke="#fbbf24" strokeWidth="2" />
          <text x="143" y="111" fill="#fcd34d" fontSize="11">hips back</text>
        </svg>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 text-center text-[11px] leading-4 text-zinc-400">
        <span className="rounded-lg bg-white/[0.035] px-2 py-2">Chest proud</span>
        <span className="rounded-lg bg-white/[0.035] px-2 py-2">Hips back</span>
        <span className="rounded-lg bg-white/[0.035] px-2 py-2">Knees follow toes</span>
      </div>
    </div>
  );
}
