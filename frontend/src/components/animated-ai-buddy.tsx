/* eslint-disable @next/next/no-img-element */

import type { WorkoutExercise } from "@/lib/workout-plan";

type AnimatedAIBuddyProps = { exercise: WorkoutExercise };

type ExerciseVisual = {
  imageUrl: string;
  sourceUrl: string;
  credit: string;
  license: string;
  alt: string;
};

const COMMONS_FILE_PATH = "https://commons.wikimedia.org/wiki/Special:FilePath/";

const exerciseVisuals: Record<WorkoutExercise["kind"], ExerciseVisual> = {
  squat: {
    imageUrl: `${COMMONS_FILE_PATH}Woman_doing_squat_workout_in_gym_with_barbell.jpg?width=1200`,
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Woman_doing_squat_workout_in_gym_with_barbell.jpg",
    credit: "Nenad Stojković",
    license: "CC BY 2.0",
    alt: "Female trainer demonstrating a squat",
  },
  push_up: {
    imageUrl: `${COMMONS_FILE_PATH}Girl_doing_push-ups.jpg?width=1200`,
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Girl_doing_push-ups.jpg",
    credit: "PTPioneer",
    license: "CC BY 2.0",
    alt: "Female trainer demonstrating a push-up",
  },
  plank: {
    imageUrl: `${COMMONS_FILE_PATH}Woman_performing_plank_exercise_at_home_gym.jpg?width=1200`,
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Woman_performing_plank_exercise_at_home_gym.jpg",
    credit: "Shixart1985",
    license: "CC BY 2.0",
    alt: "Female trainer demonstrating a forearm plank",
  },
  lunge: {
    imageUrl: `${COMMONS_FILE_PATH}Low_Lunge.jpg?width=1124`,
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Low_Lunge.jpg",
    credit: "BameSanah88",
    license: "CC BY-SA 4.0",
    alt: "Female trainer demonstrating a lunge",
  },
  glute_bridge: {
    imageUrl: `${COMMONS_FILE_PATH}Glute-bridge.png?width=1080`,
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Glute-bridge.png",
    credit: "Marianne Gilbak",
    license: "CC BY-SA 4.0",
    alt: "Trainer demonstrating a glute bridge",
  },
  mobility: {
    imageUrl: `${COMMONS_FILE_PATH}Shoulder_stretch_personal_training.jpg?width=1200`,
    sourceUrl: "https://commons.wikimedia.org/wiki/File:Shoulder_stretch_personal_training.jpg",
    credit: "PTPioneer",
    license: "CC BY 2.0",
    alt: "Female trainer demonstrating a shoulder mobility stretch",
  },
};

/** Free, exercise-aware trainer visuals kept separate from live camera analysis. */
export function AnimatedAIBuddy({ exercise }: AnimatedAIBuddyProps) {
  const visual = exerciseVisuals[exercise.kind];

  return (
    <div className="relative min-h-[330px] overflow-hidden bg-[#071016]">
      <img
        key={exercise.id}
        src={visual.imageUrl}
        alt={visual.alt}
        className="absolute inset-0 h-full w-full object-cover object-center"
      />
      <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(3,10,15,0.08)_20%,rgba(3,10,15,0.4)_66%,rgba(3,10,15,0.94)_100%)]" />

      <div className="absolute left-4 top-4 rounded-full border border-cyan-200/25 bg-[#061018]/80 px-3 py-1.5 text-xs font-semibold text-cyan-100 backdrop-blur">
        AI Buddy demonstration
      </div>

      <div className="absolute inset-x-4 bottom-4 flex items-end justify-between gap-3">
        <p className="max-w-[14rem] text-sm font-medium leading-5 text-white drop-shadow">Copy the position shown, then let the camera check your form.</p>
        <a href={visual.sourceUrl} target="_blank" rel="noreferrer" className="max-w-[11rem] rounded-lg border border-white/15 bg-black/55 px-2.5 py-2 text-right text-[10px] leading-4 text-zinc-300 backdrop-blur transition hover:border-cyan-200/40 hover:text-cyan-100">
          Photo: {visual.credit} · {visual.license}
        </a>
      </div>
    </div>
  );
}
