import {
  getAccessToken,
  setAccessToken,
  clearAccessToken,
  type AuthTokenResponse,
} from "@/lib/auth";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "/api/backend";

export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(
    status: number,
    detail: string,
  ) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function parseResponse(
  response: Response,
): Promise<unknown> {
  const contentType =
    response.headers.get("content-type") ?? "";

  if (
    contentType.includes(
      "application/json",
    )
  ) {
    return response.json();
  }

  return response.text();
}

function getErrorDetail(
  payload: unknown,
): string {
  if (
    typeof payload === "object" &&
    payload !== null &&
    "detail" in payload
  ) {
    const detail = (
      payload as {
        detail?: unknown;
      }
    ).detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          if (
            typeof item === "object" &&
            item !== null &&
            "msg" in item
          ) {
            const message = (
              item as {
                msg?: unknown;
              }
            ).msg;

            return typeof message === "string"
              ? message
              : "Validation error";
          }

          return "Validation error";
        })
        .join(", ");
    }
  }

  return "The request could not be completed.";
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const token = getAccessToken();

  const headers = new Headers(
    options.headers,
  );

  if (!headers.has("Accept")) {
    headers.set(
      "Accept",
      "application/json",
    );
  }

  if (
    options.body &&
    !(options.body instanceof FormData) &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  if (token) {
    headers.set(
      "Authorization",
      `Bearer ${token}`,
    );
  }

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers,
    },
  );

  const payload =
    await parseResponse(response);

  if (!response.ok) {
    if (response.status === 401) {
      clearAccessToken();
    }

    throw new ApiError(
      response.status,
      getErrorDetail(payload),
    );
  }

  return payload as T;
}

export type LoginRequest = {
  username: string;
  password: string;
};

export async function login(
  credentials: LoginRequest,
): Promise<AuthTokenResponse> {
  const body =
    new URLSearchParams();

  body.set(
    "username",
    credentials.username,
  );

  body.set(
    "password",
    credentials.password,
  );

  const response = await fetch(
    `${API_BASE_URL}/auth/login`,
    {
      method: "POST",
      headers: {
        Accept:
          "application/json",
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
      body: body.toString(),
    },
  );

  const payload =
    await parseResponse(response);

  if (!response.ok) {
    throw new ApiError(
      response.status,
      getErrorDetail(payload),
    );
  }

  const tokenResponse =
    payload as AuthTokenResponse;

  setAccessToken(
    tokenResponse.access_token,
  );

  return tokenResponse;
}

export function logout(): void {
  clearAccessToken();
}

export type CurrentUser = {
  id: number;
  full_name: string;
  email: string;
  age: number | null;
  height_cm: number | null;
  weight_kg: number | null;
  sex: string | null;
  fitness_goal: string | null;
  dietary_preference: string | null;
  activity_level: string | null;
  workout_preference: string | null;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
};

export async function getCurrentUser(): Promise<CurrentUser> {
  return apiRequest<CurrentUser>(
    "/auth/me",
  );
}

export type RegisterUserRequest = {
  full_name: string;
  email: string;
  password: string;
};

export type ProfileUpdateRequest = {
  full_name?: string;
  age?: number;
  height_cm?: number;
  weight_kg?: number;
  sex?: string;
  fitness_goal?: string;
  dietary_preference?: string;
  activity_level?: string;
  workout_preference?: string;
};

export async function registerUser(
  details: RegisterUserRequest,
): Promise<CurrentUser> {
  return apiRequest<CurrentUser>(
    "/auth/register",
    {
      method: "POST",
      body: JSON.stringify(details),
    },
  );
}

export async function updateCurrentUser(
  details: ProfileUpdateRequest,
): Promise<CurrentUser> {
  return apiRequest<CurrentUser>(
    "/auth/me",
    {
      method: "PATCH",
      body: JSON.stringify(details),
    },
  );
}

export type AdminSummary = {
  users: {
    total_users: number;
    active_users: number;
    inactive_users: number;
    admin_users: number;
  };
  workouts: {
    total_workouts: number;
    total_repetitions: number;
    average_performance_score: number;
    best_performance_score: number;
  };
  nutrition: {
    total_food_entries: number;
    total_calories: number;
    total_protein_g: number;
    total_carbohydrates_g: number;
    total_fat_g: number;
  };
  chat: {
    total_sessions: number;
    total_messages: number;
    user_messages: number;
    assistant_messages: number;
  };
  smart_gym: {
    equipment_count: number;
    telemetry_samples: number;
    total_commands: number;
    increase_commands: number;
    decrease_commands: number;
  };
};

export async function getAdminSummary(): Promise<AdminSummary> {
  return apiRequest<AdminSummary>(
    "/admin/summary",
  );
}

export type AdminUser = {
  id: number;
  full_name: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
};

export type AdminUserList = {
  items: AdminUser[];
  total: number;
  limit: number;
  offset: number;
};

export async function getAdminUsers(
  limit = 100,
  offset = 0,
): Promise<AdminUserList> {
  return apiRequest<AdminUserList>(
    `/admin/users?limit=${limit}&offset=${offset}`,
  );
}

export async function updateAdminUserStatus(
  userId: number,
  isActive: boolean,
): Promise<AdminUser> {
  return apiRequest<AdminUser>(
    `/admin/users/${userId}/status`,
    {
      method: "PATCH",
      body: JSON.stringify({
        is_active: isActive,
      }),
    },
  );
}

export type WorkoutAnalytics = {
  total_workouts: number;
  total_repetitions: number;
  average_performance_score: number;
  best_performance_score: number;
};

export type NutritionAnalytics = {
  total_food_entries: number;
  total_calories: number;
  total_protein_g: number;
  total_carbohydrates_g: number;
  total_fat_g: number;
};

export type SmartGymAnalytics = {
  equipment_count: number;
  telemetry_samples: number;
  average_performance_score: number;
  average_fatigue_level: number;
  average_heart_rate: number;
  average_resistance: number;
  total_commands: number;
  increase_commands: number;
  decrease_commands: number;
};

export type FitnessAnalytics = {
  generated_at: string;
  workouts: WorkoutAnalytics;
  nutrition: NutritionAnalytics;
  smart_gym: SmartGymAnalytics;
};

export async function getAnalyticsSummary(): Promise<FitnessAnalytics> {
  return apiRequest<FitnessAnalytics>(
    "/analytics/summary",
  );
}

export type GymTrainerFrameAnalysis = {
  frame_number: number;
  timestamp_seconds: number;
  analysis: unknown;
};

export type GymTrainerVideoAnalysis = {
  exercise: string;
  total_frames: number;
  processed_frames: number;
  detected_frames: number;
  detection_rate: number;
  results: GymTrainerFrameAnalysis[];
};

export async function analyzeGymTrainerVideo(
  video: File,
  exercise: string,
): Promise<GymTrainerVideoAnalysis> {
  const formData = new FormData();

  formData.append(
    "video",
    video,
  );

  formData.append(
    "exercise",
    exercise,
  );

  return apiRequest<GymTrainerVideoAnalysis>(
    "/gym-trainer/video",
    {
      method: "POST",
      body: formData,
    },
  );
}

export type RepetitionPerformance = {
  repetition_number: number;
  overall_score: number;
  depth_score: number;
  posture_score: number;
  control_score: number;
  rating: string;
};

export type WorkoutSession = {
  id: number;
  exercise: string;
  total_repetitions: number;
  performance_score: number;
  best_frame_score: number;
  worst_frame_score: number;
  depth_score: number;
  posture_score: number;
  control_score: number;
  average_repetition_score: number;
  best_repetition_score: number;
  worst_repetition_score: number;
  rating: string;
  warnings: string | null;
  started_at: string;
  completed_at: string;
};

export type GymTrainerPerformanceVideo = {
  exercise: string;
  video: {
    total_frames: number;
    processed_frames: number;
    detected_frames: number;
    detection_rate: number;
  };
  total_repetitions: number;
  performance_score: number;
  best_frame_score: number;
  worst_frame_score: number;
  depth_score: number;
  posture_score: number;
  control_score: number;
  average_repetition_score: number;
  best_repetition_score: number;
  worst_repetition_score: number;
  rating: string;
  warnings: string[];
  repetition_scores: RepetitionPerformance[];
  workout: WorkoutSession;
};

export async function analyzeGymTrainerPerformanceVideo(
  video: File,
  exercise: string,
): Promise<GymTrainerPerformanceVideo> {
  const formData = new FormData();

  formData.append(
    "video",
    video,
  );

  formData.append(
    "exercise",
    exercise,
  );

  return apiRequest<GymTrainerPerformanceVideo>(
    "/performance/video",
    {
      method: "POST",
      body: formData,
    },
  );
}

export async function getGymTrainerHealth(): Promise<{
  status: string;
  service: string;
}> {
  return apiRequest<{
    status: string;
    service: string;
  }>(
    "/gym-trainer/health",
  );
}

export type LiveTrainerSession = {
  session_id: string;
  exercise: string;
  expires_in_seconds: number;
};

export type LiveTrainerAnalysis = {
  exercise: string;
  knee_angle: number;
  phase: string;
  repetitions: number;
  depth_score: number;
  posture_score: number;
  control_score: number;
  form_score: number;
  rating: string;
  feedback: string[];
};

export type LiveTrainerLandmark = {
  x: number;
  y: number;
  visibility: number;
};

export type LiveTrainerFrame = {
  session_id: string;
  pose_detected: boolean;
  message: string;
  analysis: LiveTrainerAnalysis | null;
  landmarks: LiveTrainerLandmark[] | null;
};

export async function startLiveTrainer(): Promise<LiveTrainerSession> {
  return apiRequest<LiveTrainerSession>(
    "/gym-trainer/live/start",
    {
      method: "POST",
    },
  );
}

export async function analyzeLiveTrainerFrame(
  sessionId: string,
  image: Blob,
): Promise<LiveTrainerFrame> {
  const formData = new FormData();

  formData.append("session_id", sessionId);
  formData.append("image", image, "camera-frame.jpg");

  return apiRequest<LiveTrainerFrame>(
    "/gym-trainer/live/frame",
    {
      method: "POST",
      body: formData,
    },
  );
}

export async function stopLiveTrainer(
  sessionId: string,
): Promise<void> {
  await apiRequest<unknown>(
    `/gym-trainer/live/${sessionId}`,
    {
      method: "DELETE",
    },
  );
}

export type HabitAnalysis = {
  memory: {
    total_messages: number;
    positive_messages: number;
    negative_messages: number;
    neutral_messages: number;
    recent_sentiment: string;
    recent_emotion: string;
    recent_motivation_level: string;
    unmotivated_count: number;
    stressed_count: number;
    low_motivation_count: number;
    motivation_trend: string;
  };
  behavior: {
    consistency_score: number;
    motivation_score: number;
    emotional_stability_score: number;
    behavioral_risk_score: number;
    risk_level: string;
  };
  skip_risk: {
    probability: number;
    level: string;
    reason: string;
  };
  nudge: {
    message: string;
    urgency: string;
    action: string;
  };
  schedule: {
    action: string;
    intensity: string;
    duration_minutes: number;
    reason: string;
  };
};

export async function getHabitAnalysis(): Promise<HabitAnalysis> {
  return apiRequest<HabitAnalysis>(
    "/habits/analysis",
  );
}

export type SmartGymEquipment = {
  equipment_id: string;
  equipment_type: string;
  resistance_level: number;
  repetitions: number;
  performance_score: number;
  heart_rate: number;
  fatigue_level: number;
  last_action: string | null;
  last_command_value: number | null;
  last_command_reason: string | null;
  updated_at: string;
};

export type SmartGymStatus = {
  mqtt_connected: boolean;
  equipment_count: number;
  equipment: SmartGymEquipment[];
};

export async function getSmartGymStatus(): Promise<SmartGymStatus> {
  return apiRequest<SmartGymStatus>(
    "/iot/status",
  );
}

export type WorkoutHistory = {
  items: WorkoutSession[];
  total: number;
  limit: number;
  offset: number;
};

export async function getWorkoutHistory(
  limit = 10,
): Promise<WorkoutHistory> {
  return apiRequest<WorkoutHistory>(
    `/workouts?limit=${limit}`,
  );
}

export type WeeklyPerformance = {
  week_start: string;
  week_end: string;
  workout_count: number;
  total_repetitions: number;
  average_performance_score: number;
  best_performance_score: number;
  worst_performance_score: number;
  average_depth_score: number;
  average_posture_score: number;
  average_control_score: number;
  performance_trend: string;
  summary: string;
};

export async function getWeeklyPerformance(): Promise<WeeklyPerformance> {
  return apiRequest<WeeklyPerformance>(
    "/performance/weekly",
  );
}

export type GymCandidate = {
  name: string;
  distance_km: number;
  rating: number;
  specialties: string[];
};

export type FitnessRecommendations = {
  gyms: Array<GymCandidate & { reason: string }>;
  workouts: Array<{
    name: string;
    goal: string;
    difficulty: string;
    duration_minutes: number;
    reason: string;
  }>;
  challenges: Array<{
    name: string;
    goal: string;
    duration_days: number;
    difficulty: string;
    reason: string;
  }>;
};

export async function getFitnessRecommendations(
  maxDistanceKm: number,
  gyms: GymCandidate[],
): Promise<FitnessRecommendations> {
  return apiRequest<FitnessRecommendations>(
    "/recommendations",
    {
      method: "POST",
      body: JSON.stringify({
        gyms,
        max_distance_km: maxDistanceKm,
      }),
    },
  );
}
