import { apiRequest } from "./api";

export type DieticianCalculationRequest = {
  age: number;
  sex: string;
  height_cm: number;
  weight_kg: number;
  activity_level: string;
  goal: string;
};

export type DieticianCalculationResponse = {
  bmi: number;
  bmi_category: string;
  bmr: number;
  activity_multiplier: number;
  activity_level: string;
  calorie_target: number;
  calorie_adjustment: number;
  protein_g: number;
  carbohydrates_g: number;
  fat_g: number;
};

export type DietMeal = {
  name: string;
  calories: number;
  protein_g: number;
  carbohydrates_g: number;
  fat_g: number;
};

export type GroceryItem = {
  name: string;
  quantity: number;
  unit: string;
  category: string;
};

export type DietPlanResponse = {
  bmi: number;
  bmi_category: string;
  bmr: number;
  maintenance_calories: number;
  target_calories: number;
  meals: DietMeal[];
  grocery_list: GroceryItem[];
};

export type NutritionLogCreate = {
  food_name: string;
  quantity: number;
  calories: number;
  protein_g: number;
  carbohydrates_g: number;
  fat_g: number;
  consumed_at?: string;
};

export type NutritionLogResponse = {
  id: number;
  food_name: string;
  quantity: number;
  calories: number;
  protein_g: number;
  carbohydrates_g: number;
  fat_g: number;
  consumed_at: string;
};

export type NutritionSummaryResponse = {
  total_entries: number;
  total_calories: number;
  total_protein_g: number;
  total_carbohydrates_g: number;
  total_fat_g: number;
};

export type ChatRequest = {
  message: string;
  session_id?: number | null;
};

export type ChatResponse = {
  session_id: number;
  message_id: number;
  message: string;
  intent: string;
  sentiment: string;
  emotion: string;
  motivation_level: number;
  emotion_confidence: number;
  strategy: string;
};

export async function calculateDieticianTargets(
  payload: DieticianCalculationRequest,
): Promise<DieticianCalculationResponse> {
  return apiRequest<DieticianCalculationResponse>(
    "/dietician/calculate",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export async function generateDietPlan(
): Promise<DietPlanResponse> {
  return apiRequest<DietPlanResponse>(
    "/dietician/plan",
    {
      method: "POST",
      body: JSON.stringify({}),
    },
  );
}

export async function getDieticianHealth(): Promise<{
  status: string;
  service: string;
}> {
  return apiRequest<{
    status: string;
    service: string;
  }>("/dietician/health");
}

export async function createNutritionLog(
  payload: NutritionLogCreate,
): Promise<NutritionLogResponse> {
  return apiRequest<NutritionLogResponse>(
    "/nutrition",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}

export async function getNutritionHistory(
  limit = 20,
  offset = 0,
  foodName?: string,
): Promise<NutritionLogResponse[]> {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });

  if (foodName?.trim()) {
    params.set("food_name", foodName.trim());
  }

  return apiRequest<NutritionLogResponse[]>(
    `/nutrition?${params.toString()}`,
  );
}

export async function getNutritionSummary(): Promise<NutritionSummaryResponse> {
  return apiRequest<NutritionSummaryResponse>("/nutrition/summary");
}

export async function sendDieticianChat(
  payload: ChatRequest,
): Promise<ChatResponse> {
  return apiRequest<ChatResponse>(
    "/chat",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}
