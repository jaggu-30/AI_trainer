import type { CurrentUser } from "@/lib/api";

export type WorkoutExerciseKind =
  | "squat"
  | "push_up"
  | "plank"
  | "lunge"
  | "glute_bridge"
  | "mobility";

export type WorkoutExercise = {
  id: string;
  kind: WorkoutExerciseKind;
  name: string;
  prescription: string;
  cue: string;
};

export type WorkoutPlan = {
  dateKey: string;
  focus: string;
  goalLabel: string;
  duration: string;
  settingLabel: string;
  goalNote: string;
  warmup: string[];
  workout: string[];
  exercises: WorkoutExercise[];
  voiceIntro: string;
};

type GoalPrescription = {
  duration: string;
  note: string;
  targets: Record<WorkoutExerciseKind, string>;
};

type ExerciseDefinition = Omit<WorkoutExercise, "prescription">;

function labelText(
  value: string | null | undefined,
  fallback: string,
): string {
  if (!value) {
    return fallback;
  }

  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function localDateKey(date = new Date()): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

const DAY_PROGRAMS: Array<{
  focus: string;
  exercises: ExerciseDefinition[];
}> = [
  {
    focus: "Recovery, mobility, and core control",
    exercises: [
      {
        id: "mobility-flow",
        kind: "mobility",
        name: "Mobility flow",
        cue: "Move slowly through relaxed shoulder and hip circles.",
      },
      {
        id: "plank-hold",
        kind: "plank",
        name: "Forearm plank",
        cue: "Keep a long line from shoulders through hips to heels.",
      },
      {
        id: "glute-bridge",
        kind: "glute_bridge",
        name: "Glute bridge",
        cue: "Press through your heels and lift your hips without arching your back.",
      },
    ],
  },
  {
    focus: "Chest, shoulders, and triceps",
    exercises: [
      {
        id: "push-up",
        kind: "push_up",
        name: "Push-ups",
        cue: "Keep your body straight and lower with your elbows controlled.",
      },
      {
        id: "plank-shoulder",
        kind: "plank",
        name: "High plank hold",
        cue: "Stack shoulders over hands and keep your hips level.",
      },
      {
        id: "mobility-shoulder",
        kind: "mobility",
        name: "Shoulder mobility",
        cue: "Keep your ribs down while making smooth shoulder circles.",
      },
    ],
  },
  {
    focus: "Lower body strength",
    exercises: [
      {
        id: "squat",
        kind: "squat",
        name: "Bodyweight squats",
        cue: "Send your hips back, keep your chest proud, and track knees over toes.",
      },
      {
        id: "reverse-lunge",
        kind: "lunge",
        name: "Reverse lunges",
        cue: "Step back softly and keep your front knee stacked over the ankle.",
      },
      {
        id: "bridge-lower",
        kind: "glute_bridge",
        name: "Glute bridges",
        cue: "Squeeze your glutes at the top, then lower with control.",
      },
    ],
  },
  {
    focus: "Core stability and posture",
    exercises: [
      {
        id: "plank-core",
        kind: "plank",
        name: "Forearm plank",
        cue: "Keep your neck neutral and brace through your midsection.",
      },
      {
        id: "bridge-core",
        kind: "glute_bridge",
        name: "Glute bridges",
        cue: "Lift from the hips and keep your knees aligned.",
      },
      {
        id: "mobility-core",
        kind: "mobility",
        name: "Hip mobility flow",
        cue: "Use an easy range of motion and steady breathing.",
      },
    ],
  },
  {
    focus: "Upper-body strength and control",
    exercises: [
      {
        id: "push-up-strength",
        kind: "push_up",
        name: "Controlled push-ups",
        cue: "Lower as one unit, then press the floor away.",
      },
      {
        id: "plank-upper",
        kind: "plank",
        name: "High plank hold",
        cue: "Press through the floor and avoid letting the lower back dip.",
      },
      {
        id: "mobility-upper",
        kind: "mobility",
        name: "Upper-body mobility",
        cue: "Keep the movement smooth and pain-free.",
      },
    ],
  },
  {
    focus: "Leg stability and balance",
    exercises: [
      {
        id: "squat-tempo",
        kind: "squat",
        name: "Tempo squats",
        cue: "Take three seconds down, pause briefly, then stand tall.",
      },
      {
        id: "lunge-balance",
        kind: "lunge",
        name: "Reverse lunges",
        cue: "Keep your torso tall and push through the front foot to return.",
      },
      {
        id: "bridge-balance",
        kind: "glute_bridge",
        name: "Glute bridges",
        cue: "Keep your knees parallel as you lift and lower.",
      },
    ],
  },
  {
    focus: "Full-body fitness",
    exercises: [
      {
        id: "squat-full",
        kind: "squat",
        name: "Bodyweight squats",
        cue: "Keep your heels grounded and move with control.",
      },
      {
        id: "push-up-full",
        kind: "push_up",
        name: "Push-ups",
        cue: "Keep your hips in line with your shoulders and ankles.",
      },
      {
        id: "plank-full",
        kind: "plank",
        name: "Forearm plank",
        cue: "Stay steady and breathe through the hold.",
      },
    ],
  },
];

const GOAL_PRESCRIPTIONS: Record<string, GoalPrescription> = {
  weight_loss: {
    duration: "35 to 45 min",
    note: "Moderate volume and a steady pace support your fat-loss goal.",
    targets: {
      squat: "4 × 12 reps",
      push_up: "3 × 10 reps",
      plank: "3 × 35 sec",
      lunge: "3 × 10 reps / side",
      glute_bridge: "3 × 15 reps",
      mobility: "2 × 45 sec",
    },
  },
  weight_gain: {
    duration: "40 to 55 min",
    note: "Controlled strength work and sufficient recovery support healthy weight gain.",
    targets: {
      squat: "5 × 10 reps",
      push_up: "3 × 5 reps",
      plank: "3 × 30 sec",
      lunge: "4 × 8 reps / side",
      glute_bridge: "4 × 12 reps",
      mobility: "2 × 45 sec",
    },
  },
  muscle_gain: {
    duration: "40 to 55 min",
    note: "Use controlled repetitions and rest long enough to keep your form strong.",
    targets: {
      squat: "4 × 10 reps",
      push_up: "4 × 8 reps",
      plank: "3 × 40 sec",
      lunge: "3 × 10 reps / side",
      glute_bridge: "4 × 12 reps",
      mobility: "2 × 45 sec",
    },
  },
  maintenance: {
    duration: "25 to 40 min",
    note: "A balanced strength and mobility session supports your maintenance goal.",
    targets: {
      squat: "3 × 10 reps",
      push_up: "3 × 8 reps",
      plank: "3 × 30 sec",
      lunge: "3 × 8 reps / side",
      glute_bridge: "3 × 12 reps",
      mobility: "2 × 40 sec",
    },
  },
};

export function buildTodayPlan(
  user: CurrentUser | null,
): WorkoutPlan {
  const name = user?.full_name?.split(" ")[0] || "there";
  const date = new Date();
  const program = DAY_PROGRAMS[date.getDay()];
  const goalKey = user?.fitness_goal || "maintenance";
  const prescription =
    GOAL_PRESCRIPTIONS[goalKey] ?? GOAL_PRESCRIPTIONS.maintenance;
  const exercises = program.exercises.map((exercise) => ({
    ...exercise,
    prescription: prescription.targets[exercise.kind],
  }));

  const warmup = [
    "2 minutes of easy marching or walking in place.",
    "10 arm circles each direction and 10 hip circles.",
    "8 slow bodyweight squats to prepare your movement.",
  ];

  return {
    dateKey: localDateKey(date),
    focus: program.focus,
    goalLabel: labelText(user?.fitness_goal, "Balanced Fitness"),
    duration: prescription.duration,
    settingLabel: labelText(user?.workout_preference, "Home"),
    warmup,
    workout: exercises.map(
      (exercise) => `${exercise.prescription} — ${exercise.name}`,
    ),
    exercises,
    goalNote: prescription.note,
    voiceIntro: `Hi ${name}. Today is ${program.focus}. ${prescription.note} Start with ${warmup[0]} Then complete ${exercises[0].prescription} of ${exercises[0].name}.`,
  };
}
