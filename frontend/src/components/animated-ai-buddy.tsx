import type { WorkoutExercise } from "@/lib/workout-plan";

type AnimatedAIBuddyProps = {
  exercise: WorkoutExercise;
};

const SKIN = "#d9a184";
const SKIN_SHADOW = "#b97561";
const HAIR = "#241a20";
const TOP = "#22c7da";
const TOP_SHADOW = "#127d95";
const LEGGINGS = "#263340";
const LEGGINGS_SHADOW = "#111a24";

function Head({ x, y }: { x: number; y: number }) {
  return (
    <g transform={`translate(${x} ${y})`}>
      <ellipse cx="0" cy="4" rx="22" ry="27" fill={SKIN} />
      <path d="M-23 0C-23-27 22-32 24 2C13-9-7-15-23 0Z" fill={HAIR} />
      <path d="M-19-6C-8-18 8-17 20-4" fill="none" stroke="#3b2830" strokeLinecap="round" strokeWidth="7" />
      <circle cx="-8" cy="4" r="2" fill="#29313c" />
      <circle cx="8" cy="4" r="2" fill="#29313c" />
      <path d="M-5 16Q0 20 5 16" fill="none" stroke={SKIN_SHADOW} strokeLinecap="round" strokeWidth="2" />
      <circle cx="19" cy="-21" r="13" fill={HAIR} />
    </g>
  );
}

function Arm({
  x,
  y,
  rotation,
  values,
  duration = "2.8s",
}: {
  x: number;
  y: number;
  rotation: number;
  values?: string;
  duration?: string;
}) {
  return (
    <g transform={`translate(${x} ${y})`}>
      <g>
        {values && (
          <animateTransform
            attributeName="transform"
            type="rotate"
            values={values}
            dur={duration}
            repeatCount="indefinite"
          />
        )}
        {!values && <g transform={`rotate(${rotation})`} />}
        <g transform={values ? undefined : `rotate(${rotation})`}>
          <rect x="-10" y="0" width="20" height="55" rx="10" fill={SKIN} />
          <rect x="-9" y="48" width="18" height="49" rx="9" fill={SKIN} />
          <circle cx="0" cy="98" r="11" fill={SKIN} />
          <path d="M-6 55H6" stroke={SKIN_SHADOW} strokeWidth="2" />
        </g>
      </g>
    </g>
  );
}

function SquatModel() {
  return (
    <g>
      <ellipse cx="200" cy="445" rx="142" ry="19" fill="#0b1d29" opacity="0.75" />
      <g transform="translate(200 102)">
        <animateTransform attributeName="transform" type="translate" values="200 102;200 124;200 102" dur="3.2s" repeatCount="indefinite" />
        <Head x={0} y={-49} />
        <path d="M-47 2Q0-19 47 2L42 107Q0 129-42 107Z" fill={TOP} />
        <path d="M-38 7Q0-5 38 7L35 33Q0 24-35 33Z" fill={TOP_SHADOW} opacity="0.5" />
        <path d="M-39 102Q0 116 39 102L46 128Q0 143-46 128Z" fill={LEGGINGS} />
        <Arm x={-43} y={13} rotation={-64} values="-64 0 0;-94 0 0;-64 0 0" duration="3.2s" />
        <Arm x={43} y={13} rotation={64} values="64 0 0;94 0 0;64 0 0" duration="3.2s" />
        <g transform="translate(-28 122)">
          <animateTransform attributeName="transform" type="rotate" values="-4 0 0;-48 0 0;-4 0 0" dur="3.2s" repeatCount="indefinite" />
          <rect x="-16" y="0" width="32" height="88" rx="16" fill={LEGGINGS} />
          <g transform="translate(0 75)">
            <animateTransform attributeName="transform" type="rotate" values="4 0 0;48 0 0;4 0 0" dur="3.2s" repeatCount="indefinite" />
            <rect x="-14" y="0" width="28" height="91" rx="14" fill={LEGGINGS_SHADOW} />
            <path d="M-16 84Q0 76 30 91L28 106H-18Z" fill="#e1eef0" />
          </g>
        </g>
        <g transform="translate(28 122)">
          <animateTransform attributeName="transform" type="rotate" values="4 0 0;48 0 0;4 0 0" dur="3.2s" repeatCount="indefinite" />
          <rect x="-16" y="0" width="32" height="88" rx="16" fill={LEGGINGS} />
          <g transform="translate(0 75)">
            <animateTransform attributeName="transform" type="rotate" values="-4 0 0;-48 0 0;-4 0 0" dur="3.2s" repeatCount="indefinite" />
            <rect x="-14" y="0" width="28" height="91" rx="14" fill={LEGGINGS_SHADOW} />
            <path d="M-29 91Q0 76 16 84L18 106H-28Z" fill="#e1eef0" />
          </g>
        </g>
      </g>
    </g>
  );
}

function PushUpModel() {
  return (
    <g transform="translate(20 52)">
      <ellipse cx="192" cy="365" rx="164" ry="18" fill="#0b1d29" opacity="0.75" />
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 0;0 32;0 0" dur="2.7s" repeatCount="indefinite" />
        <path d="M100 150Q120 108 173 124L289 187Q306 198 301 219L283 239L150 194Q111 179 100 150Z" fill={TOP} />
        <path d="M144 181L283 239L273 265L132 210Z" fill={LEGGINGS} />
        <path d="M274 260L341 315L331 332L254 278Z" fill={LEGGINGS_SHADOW} />
        <path d="M331 316L358 337L345 350L320 330Z" fill="#e1eef0" />
        <Head x={100} y={139} />
        <g transform="translate(145 181)">
          <animateTransform attributeName="transform" type="rotate" values="50 0 0;88 0 0;50 0 0" dur="2.7s" repeatCount="indefinite" />
          <rect x="-10" y="0" width="20" height="58" rx="10" fill={SKIN} />
          <g transform="translate(0 52)">
            <animateTransform attributeName="transform" type="rotate" values="-36 0 0;-84 0 0;-36 0 0" dur="2.7s" repeatCount="indefinite" />
            <rect x="-9" y="0" width="18" height="62" rx="9" fill={SKIN} />
            <ellipse cx="4" cy="62" rx="14" ry="8" fill={SKIN} />
          </g>
        </g>
        <g transform="translate(176 196)">
          <animateTransform attributeName="transform" type="rotate" values="50 0 0;88 0 0;50 0 0" dur="2.7s" repeatCount="indefinite" />
          <rect x="-10" y="0" width="20" height="58" rx="10" fill={SKIN} />
          <g transform="translate(0 52)">
            <animateTransform attributeName="transform" type="rotate" values="-36 0 0;-84 0 0;-36 0 0" dur="2.7s" repeatCount="indefinite" />
            <rect x="-9" y="0" width="18" height="62" rx="9" fill={SKIN} />
            <ellipse cx="4" cy="62" rx="14" ry="8" fill={SKIN} />
          </g>
        </g>
      </g>
    </g>
  );
}

function PlankModel() {
  return (
    <g transform="translate(20 64)">
      <ellipse cx="200" cy="354" rx="163" ry="17" fill="#0b1d29" opacity="0.75" />
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 0;0 5;0 0" dur="2.4s" repeatCount="indefinite" />
        <path d="M104 143Q122 112 166 124L293 184Q307 194 303 214L280 237L147 195Q116 184 104 143Z" fill={TOP} />
        <path d="M145 181L285 239L274 265L131 211Z" fill={LEGGINGS} />
        <path d="M274 260L344 310L334 329L256 278Z" fill={LEGGINGS_SHADOW} />
        <path d="M334 311L360 330L347 343L322 327Z" fill="#e1eef0" />
        <Head x={104} y={134} />
        <g transform="translate(145 181) rotate(60)">
          <rect x="-10" y="0" width="20" height="61" rx="10" fill={SKIN} />
          <rect x="-9" y="56" width="18" height="56" rx="9" fill={SKIN} />
          <ellipse cx="4" cy="111" rx="15" ry="8" fill={SKIN} />
        </g>
        <g transform="translate(176 196) rotate(60)">
          <rect x="-10" y="0" width="20" height="61" rx="10" fill={SKIN} />
          <rect x="-9" y="56" width="18" height="56" rx="9" fill={SKIN} />
          <ellipse cx="4" cy="111" rx="15" ry="8" fill={SKIN} />
        </g>
      </g>
    </g>
  );
}

function LungeModel() {
  return (
    <g>
      <ellipse cx="200" cy="445" rx="142" ry="19" fill="#0b1d29" opacity="0.75" />
      <g transform="translate(200 104)">
        <animateTransform attributeName="transform" type="translate" values="200 104;200 128;200 104" dur="3s" repeatCount="indefinite" />
        <Head x={0} y={-49} />
        <path d="M-47 2Q0-19 47 2L42 107Q0 129-42 107Z" fill={TOP} />
        <path d="M-39 102Q0 116 39 102L46 128Q0 143-46 128Z" fill={LEGGINGS} />
        <Arm x={-43} y={13} rotation={-10} values="-10 0 0;-18 0 0;-10 0 0" duration="3s" />
        <Arm x={43} y={13} rotation={10} values="10 0 0;18 0 0;10 0 0" duration="3s" />
        <g transform="translate(-28 122)">
          <animateTransform attributeName="transform" type="rotate" values="8 0 0;2 0 0;8 0 0" dur="3s" repeatCount="indefinite" />
          <rect x="-16" y="0" width="32" height="95" rx="16" fill={LEGGINGS} />
          <rect x="-14" y="82" width="28" height="86" rx="14" fill={LEGGINGS_SHADOW} />
          <path d="M-18 160Q0 151 30 167L28 181H-20Z" fill="#e1eef0" />
        </g>
        <g transform="translate(28 122)">
          <animateTransform attributeName="transform" type="rotate" values="-12 0 0;58 0 0;-12 0 0" dur="3s" repeatCount="indefinite" />
          <rect x="-16" y="0" width="32" height="92" rx="16" fill={LEGGINGS} />
          <g transform="translate(0 82)">
            <animateTransform attributeName="transform" type="rotate" values="-8 0 0;-70 0 0;-8 0 0" dur="3s" repeatCount="indefinite" />
            <rect x="-14" y="0" width="28" height="84" rx="14" fill={LEGGINGS_SHADOW} />
            <path d="M-29 77Q0 67 17 82L20 96H-28Z" fill="#e1eef0" />
          </g>
        </g>
      </g>
    </g>
  );
}

function GluteBridgeModel() {
  return (
    <g transform="translate(14 30)">
      <ellipse cx="197" cy="397" rx="166" ry="18" fill="#0b1d29" opacity="0.75" />
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 34;0 0;0 34" dur="3s" repeatCount="indefinite" />
        <path d="M105 267Q110 225 152 220L246 208Q276 209 282 233L253 276L141 291Q113 292 105 267Z" fill={TOP} />
        <path d="M247 208L292 233L275 272L228 259Z" fill={LEGGINGS} />
        <path d="M286 240L341 317L320 332L255 273Z" fill={LEGGINGS_SHADOW} />
        <path d="M320 316L357 330L348 347L309 334Z" fill="#e1eef0" />
        <Head x={101} y={254} />
        <g transform="translate(142 280) rotate(74)">
          <rect x="-10" y="0" width="20" height="64" rx="10" fill={SKIN} />
          <ellipse cx="6" cy="64" rx="15" ry="8" fill={SKIN} />
        </g>
        <g transform="translate(166 276) rotate(74)">
          <rect x="-10" y="0" width="20" height="64" rx="10" fill={SKIN} />
          <ellipse cx="6" cy="64" rx="15" ry="8" fill={SKIN} />
        </g>
      </g>
    </g>
  );
}

function MobilityModel() {
  return (
    <g>
      <ellipse cx="200" cy="445" rx="142" ry="19" fill="#0b1d29" opacity="0.75" />
      <g transform="translate(200 102)">
        <Head x={0} y={-49} />
        <path d="M-47 2Q0-19 47 2L42 107Q0 129-42 107Z" fill={TOP} />
        <path d="M-39 102Q0 116 39 102L46 128Q0 143-46 128Z" fill={LEGGINGS} />
        <Arm x={-43} y={13} rotation={-110} values="-110 0 0;48 0 0;250 0 0;410 0 0" duration="4s" />
        <Arm x={43} y={13} rotation={110} values="110 0 0;-48 0 0;-250 0 0;-410 0 0" duration="4s" />
        <g transform="translate(-28 122)">
          <rect x="-16" y="0" width="32" height="88" rx="16" fill={LEGGINGS} />
          <rect x="-14" y="76" width="28" height="91" rx="14" fill={LEGGINGS_SHADOW} />
          <path d="M-18 160Q0 151 30 167L28 181H-20Z" fill="#e1eef0" />
        </g>
        <g transform="translate(28 122)">
          <rect x="-16" y="0" width="32" height="88" rx="16" fill={LEGGINGS} />
          <rect x="-14" y="76" width="28" height="91" rx="14" fill={LEGGINGS_SHADOW} />
          <path d="M-30 167Q0 151 18 160L20 181H-28Z" fill="#e1eef0" />
        </g>
      </g>
    </g>
  );
}

function Movement({ kind }: { kind: WorkoutExercise["kind"] }) {
  switch (kind) {
    case "push_up":
      return <PushUpModel />;
    case "plank":
      return <PlankModel />;
    case "lunge":
      return <LungeModel />;
    case "glute_bridge":
      return <GluteBridgeModel />;
    case "mobility":
      return <MobilityModel />;
    default:
      return <SquatModel />;
  }
}

export function AnimatedAIBuddy({ exercise }: AnimatedAIBuddyProps) {
  return (
    <div className="relative h-full min-h-[330px] overflow-hidden bg-[radial-gradient(circle_at_50%_12%,rgba(34,211,238,0.2),transparent_37%),linear-gradient(180deg,#0c1721_0%,#071016_100%)]">
      <svg viewBox="0 0 400 480" role="img" aria-label={`Animated female AI Buddy demonstrating ${exercise.name}`} className="h-full w-full" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="buddyFloor" x1="0" x2="1" y1="0" y2="1">
            <stop stopColor="#16445d" stopOpacity="0.35" />
            <stop offset="1" stopColor="#071016" stopOpacity="0" />
          </linearGradient>
        </defs>
        <rect width="400" height="480" fill="url(#buddyFloor)" opacity="0.65" />
        <Movement kind={exercise.kind} />
      </svg>
    </div>
  );
}
