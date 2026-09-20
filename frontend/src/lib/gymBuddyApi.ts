import { apiRequest } from "./api";

export type GymBuddyChatRequest = {
  message: string;
  session_id?: number | null;
};

export type GymBuddyChatResponse = {
  session_id: number;
  message_id: number;
  message: string;
  intent: string;
  sentiment: string | null;
  emotion: string | null;
  motivation_level: string | null;
  emotion_confidence: number | null;
  strategy: string | null;
};

export type ChatSession = {
  id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
};

export type ChatSessionListResponse = {
  items: ChatSession[];
  total: number;
};

export type ChatMessage = {
  id: number;
  session_id: number;
  role: string;
  content: string;
  intent: string | null;
  sentiment: string | null;
  emotion: string | null;
  motivation_level: string | null;
  emotion_confidence: number | null;
  strategy: string | null;
  created_at: string;
};

export type ChatHistoryResponse = {
  session: ChatSession;
  messages: ChatMessage[];
};

export async function sendGymBuddyMessage(
  payload: GymBuddyChatRequest,
): Promise<GymBuddyChatResponse> {
  return apiRequest<GymBuddyChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function createGymBuddySession(
  title?: string,
): Promise<ChatSession> {
  return apiRequest<ChatSession>("/chat/sessions", {
    method: "POST",
    body: JSON.stringify({
      title: title?.trim() || null,
    }),
  });
}

export async function getGymBuddySessions(
  limit = 20,
  offset = 0,
): Promise<ChatSessionListResponse> {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });

  return apiRequest<ChatSessionListResponse>(
    `/chat/sessions?${params.toString()}`,
  );
}

export async function getGymBuddySessionHistory(
  sessionId: number,
): Promise<ChatHistoryResponse> {
  return apiRequest<ChatHistoryResponse>(
    `/chat/sessions/${sessionId}`,
  );
}

export async function deleteGymBuddySession(
  sessionId: number,
): Promise<void> {
  await apiRequest<void>(
    `/chat/sessions/${sessionId}`,
    {
      method: "DELETE",
    },
  );
}
