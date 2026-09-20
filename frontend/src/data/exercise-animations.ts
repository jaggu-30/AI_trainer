export type ExerciseAnimationMode = "repetition" | "timed";

export type ExerciseAnimationDefinition = {
  id: string;
  name: string;
  category: "strength" | "cardio" | "core" | "mobility";
  animationClip: string;
  fallbackClips: string[];
  mode: ExerciseAnimationMode;
  defaultDurationSeconds: number;
  defaultReps: number | null;
  targetMuscles: string[];
  instructions: string[];
};

export const FITNESS_TRAINER_MODEL_URL = "/models/fitness-trainer.glb";
export const DEFAULT_ANIMATION_SPEED = 1;
export const ANIMATION_SPEED_OPTIONS = [0.5, 0.75, 1, 1.25, 1.5] as const;

/**
 * One source of truth for the rigged-avatar animation system. The clip names
 * are matched case-insensitively, then checked against fallback names so
 * a licensed trainer GLB can use sensible equivalent names.
 */
export const EXERCISE_ANIMATIONS: Record<string, ExerciseAnimationDefinition> = {
  squat: {
    id: "squat",
    name: "Squat",
    category: "strength",
    animationClip: "Squat",
    fallbackClips: ["BodyweightSquat", "AirSquat"],
    mode: "repetition",
    defaultDurationSeconds: 75,
    defaultReps: 12,
    targetMuscles: ["Quadriceps", "Glutes", "Hamstrings", "Core"],
    instructions: ["Hips back", "Knees follow toes", "Stand tall with control"],
  },
  jumping_jack: {
    id: "jumping_jack",
    name: "Jumping Jack",
    category: "cardio",
    animationClip: "JumpingJack",
    fallbackClips: ["Jumping Jacks", "JumpJack"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 20,
    targetMuscles: ["Shoulders", "Calves", "Cardiovascular system"],
    instructions: ["Land softly", "Move arms and legs together", "Keep a steady rhythm"],
  },
  lunge: {
    id: "lunge",
    name: "Lunge",
    category: "strength",
    animationClip: "Lunge",
    fallbackClips: ["ReverseLunge", "ForwardLunge"],
    mode: "repetition",
    defaultDurationSeconds: 75,
    defaultReps: 10,
    targetMuscles: ["Quadriceps", "Glutes", "Hamstrings"],
    instructions: ["Torso tall", "Knee over ankle", "Push through the front foot"],
  },
  push_up: {
    id: "push_up",
    name: "Push-up",
    category: "strength",
    animationClip: "PushUp",
    fallbackClips: ["Pushup", "PressUp"],
    mode: "repetition",
    defaultDurationSeconds: 75,
    defaultReps: 10,
    targetMuscles: ["Chest", "Triceps", "Shoulders", "Core"],
    instructions: ["Keep a straight body line", "Lower with control", "Press the floor away"],
  },
  plank: {
    id: "plank",
    name: "Plank",
    category: "core",
    animationClip: "Plank",
    fallbackClips: ["ForearmPlank", "HighPlank"],
    mode: "timed",
    defaultDurationSeconds: 35,
    defaultReps: null,
    targetMuscles: ["Core", "Shoulders", "Glutes"],
    instructions: ["Brace your core", "Keep hips level", "Breathe steadily"],
  },
  high_knees: {
    id: "high_knees",
    name: "High Knees",
    category: "cardio",
    animationClip: "HighKnees",
    fallbackClips: ["HighKneeRun", "RunningHighKnees"],
    mode: "repetition",
    defaultDurationSeconds: 45,
    defaultReps: 30,
    targetMuscles: ["Hip flexors", "Quadriceps", "Core"],
    instructions: ["Drive knees upward", "Stay tall", "Land lightly"],
  },
  mountain_climber: {
    id: "mountain_climber",
    name: "Mountain Climber",
    category: "cardio",
    animationClip: "MountainClimber",
    fallbackClips: ["Mountain Climbers", "PlankRun"],
    mode: "repetition",
    defaultDurationSeconds: 45,
    defaultReps: 24,
    targetMuscles: ["Core", "Shoulders", "Hip flexors"],
    instructions: ["Hands below shoulders", "Keep hips controlled", "Drive one knee at a time"],
  },
  bicep_curl: {
    id: "bicep_curl",
    name: "Bicep Curl",
    category: "strength",
    animationClip: "BicepCurl",
    fallbackClips: ["BicepsCurl", "DumbbellCurl"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 12,
    targetMuscles: ["Biceps", "Forearms"],
    instructions: ["Keep upper arms stable", "Curl smoothly", "Lower slowly"],
  },
  shoulder_press: {
    id: "shoulder_press",
    name: "Shoulder Press",
    category: "strength",
    animationClip: "ShoulderPress",
    fallbackClips: ["OverheadPress", "DumbbellShoulderPress"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 10,
    targetMuscles: ["Shoulders", "Triceps"],
    instructions: ["Brace your core", "Press overhead", "Avoid leaning back"],
  },
  tricep_extension: {
    id: "tricep_extension",
    name: "Tricep Extension",
    category: "strength",
    animationClip: "TricepExtension",
    fallbackClips: ["OverheadTricepExtension", "TricepsExtension"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 12,
    targetMuscles: ["Triceps"],
    instructions: ["Keep elbows stable", "Extend fully with control", "Avoid arching your back"],
  },
  glute_bridge: {
    id: "glute_bridge",
    name: "Glute Bridge",
    category: "strength",
    animationClip: "GluteBridge",
    fallbackClips: ["Bridge", "HipBridge"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 15,
    targetMuscles: ["Glutes", "Hamstrings", "Core"],
    instructions: ["Press through heels", "Squeeze glutes", "Lower under control"],
  },
  side_lunge: {
    id: "side_lunge",
    name: "Side Lunge",
    category: "strength",
    animationClip: "SideLunge",
    fallbackClips: ["LateralLunge"],
    mode: "repetition",
    defaultDurationSeconds: 75,
    defaultReps: 10,
    targetMuscles: ["Glutes", "Adductors", "Quadriceps"],
    instructions: ["Hips back", "Keep the other leg long", "Stay balanced"],
  },
  calf_raise: {
    id: "calf_raise",
    name: "Calf Raise",
    category: "strength",
    animationClip: "CalfRaise",
    fallbackClips: ["CalfRaises", "StandingCalfRaise"],
    mode: "repetition",
    defaultDurationSeconds: 50,
    defaultReps: 15,
    targetMuscles: ["Calves"],
    instructions: ["Rise evenly", "Pause at the top", "Lower slowly"],
  },
  crunch: {
    id: "crunch",
    name: "Crunch",
    category: "core",
    animationClip: "Crunch",
    fallbackClips: ["AbCrunch"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 15,
    targetMuscles: ["Abdominals"],
    instructions: ["Lift through the ribs", "Keep your neck relaxed", "Lower with control"],
  },
  sit_up: {
    id: "sit_up",
    name: "Sit-up",
    category: "core",
    animationClip: "SitUp",
    fallbackClips: ["Situp"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 12,
    targetMuscles: ["Abdominals", "Hip flexors"],
    instructions: ["Move smoothly", "Keep feet grounded", "Do not pull the neck"],
  },
  leg_raise: {
    id: "leg_raise",
    name: "Leg Raise",
    category: "core",
    animationClip: "LegRaise",
    fallbackClips: ["LyingLegRaise"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 12,
    targetMuscles: ["Lower abdominals", "Hip flexors"],
    instructions: ["Keep your lower back controlled", "Lift slowly", "Avoid swinging"],
  },
  russian_twist: {
    id: "russian_twist",
    name: "Russian Twist",
    category: "core",
    animationClip: "RussianTwist",
    fallbackClips: ["RussianTwists", "SeatedTwist"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 20,
    targetMuscles: ["Obliques", "Abdominals"],
    instructions: ["Rotate through the ribs", "Keep the chest lifted", "Move evenly side to side"],
  },
  burpee: {
    id: "burpee",
    name: "Burpee",
    category: "cardio",
    animationClip: "Burpee",
    fallbackClips: ["Burpees"],
    mode: "repetition",
    defaultDurationSeconds: 75,
    defaultReps: 8,
    targetMuscles: ["Full body", "Cardiovascular system"],
    instructions: ["Step or jump back safely", "Keep the core engaged", "Land softly"],
  },
  front_raise: {
    id: "front_raise",
    name: "Front Raise",
    category: "strength",
    animationClip: "FrontRaise",
    fallbackClips: ["DumbbellFrontRaise"],
    mode: "repetition",
    defaultDurationSeconds: 55,
    defaultReps: 12,
    targetMuscles: ["Front shoulders"],
    instructions: ["Lift to shoulder height", "Keep a small elbow bend", "Lower slowly"],
  },
  lateral_raise: {
    id: "lateral_raise",
    name: "Lateral Raise",
    category: "strength",
    animationClip: "LateralRaise",
    fallbackClips: ["DumbbellLateralRaise", "SideRaise"],
    mode: "repetition",
    defaultDurationSeconds: 55,
    defaultReps: 12,
    targetMuscles: ["Side shoulders"],
    instructions: ["Raise with control", "Keep shoulders down", "Avoid swinging"],
  },
  chest_press: {
    id: "chest_press",
    name: "Chest Press",
    category: "strength",
    animationClip: "ChestPress",
    fallbackClips: ["DumbbellChestPress", "BenchPress"],
    mode: "repetition",
    defaultDurationSeconds: 65,
    defaultReps: 10,
    targetMuscles: ["Chest", "Triceps", "Shoulders"],
    instructions: ["Set shoulders down", "Press evenly", "Control the return"],
  },
  deadlift: {
    id: "deadlift",
    name: "Deadlift",
    category: "strength",
    animationClip: "Deadlift",
    fallbackClips: ["RomanianDeadlift", "RDL"],
    mode: "repetition",
    defaultDurationSeconds: 75,
    defaultReps: 10,
    targetMuscles: ["Hamstrings", "Glutes", "Back"],
    instructions: ["Hinge at the hips", "Keep the spine long", "Stand with glutes"],
  },
  hip_thrust: {
    id: "hip_thrust",
    name: "Hip Thrust",
    category: "strength",
    animationClip: "HipThrust",
    fallbackClips: ["HipThrusts"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 12,
    targetMuscles: ["Glutes", "Hamstrings"],
    instructions: ["Drive through heels", "Keep ribs stacked", "Squeeze at the top"],
  },
  bicycle_crunch: {
    id: "bicycle_crunch",
    name: "Bicycle Crunch",
    category: "core",
    animationClip: "BicycleCrunch",
    fallbackClips: ["BicycleCrunches"],
    mode: "repetition",
    defaultDurationSeconds: 60,
    defaultReps: 20,
    targetMuscles: ["Obliques", "Abdominals", "Hip flexors"],
    instructions: ["Rotate gently", "Keep a steady rhythm", "Avoid pulling the neck"],
  },
  wall_sit: {
    id: "wall_sit",
    name: "Wall Sit",
    category: "strength",
    animationClip: "WallSit",
    fallbackClips: ["WallSitHold"],
    mode: "timed",
    defaultDurationSeconds: 40,
    defaultReps: null,
    targetMuscles: ["Quadriceps", "Glutes", "Core"],
    instructions: ["Back supported", "Knees around ninety degrees", "Breathe steadily"],
  },
};

export function getExerciseAnimation(
  id: string,
): ExerciseAnimationDefinition {
  return EXERCISE_ANIMATIONS[id] ?? EXERCISE_ANIMATIONS.squat;
}

export function findModelAnimationClip(
  availableClipNames: string[],
  exerciseId: string,
): string | null {
  const definition = getExerciseAnimation(exerciseId);
  const desiredNames = [definition.animationClip, ...definition.fallbackClips];

  return (
    desiredNames
      .map((desiredName) =>
        availableClipNames.find(
          (clipName) => clipName.toLowerCase() === desiredName.toLowerCase(),
        ),
      )
      .find(Boolean) ?? null
  );
}
