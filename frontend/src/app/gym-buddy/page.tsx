"use client";

import {
  Activity,
  Bot,
  CheckCircle2,
  ChevronLeft,
  Clock3,
  Heart,
  History,
  Loader2,
  MessageCircle,
  Plus,
  RefreshCw,
  Send,
  Smile,
  Sparkles,
  Trash2,
  UserRound,
  XCircle,
} from "lucide-react";
import { FormEvent, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { getCurrentUser } from "@/lib/api";
import type { CurrentUser } from "@/lib/api";

import {
  createGymBuddySession,
  deleteGymBuddySession,
  getGymBuddySessionHistory,
  getGymBuddySessions,
  sendGymBuddyMessage,
  type ChatMessage,
  type ChatSession,
  type GymBuddyChatResponse,
} from "@/lib/gymBuddyApi";

function formatDate(value: string) {
  return new Date(value).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

function formatTime(value: string) {
  return new Date(value).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

function labelText(value: string | null | undefined) {
  if (!value) {
    return "Not detected";
  }

  return value
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

function getMetricTone(value: string | null | undefined) {
  const normalized = value?.toLowerCase() ?? "";

  if (
    normalized.includes("positive") ||
    normalized.includes("happy") ||
    normalized.includes("motivated") ||
    normalized.includes("confident") ||
    normalized.includes("support")
  ) {
    return "border-emerald-400/20 bg-emerald-400/10 text-emerald-300";
  }

  if (
    normalized.includes("negative") ||
    normalized.includes("sad") ||
    normalized.includes("stress") ||
    normalized.includes("angry") ||
    normalized.includes("anxious")
  ) {
    return "border-amber-400/20 bg-amber-400/10 text-amber-300";
  }

  return "border-cyan-400/20 bg-cyan-400/10 text-cyan-300";
}

function MessageBubble({
  message,
}: {
  message: ChatMessage;
}) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex gap-3 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-cyan-400/15 bg-cyan-400/10">
          <Bot size={17} className="text-cyan-300" />
        </div>
      )}

      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 ${
          isUser
            ? "rounded-tr-sm border border-cyan-400/15 bg-cyan-400/[0.08]"
            : "rounded-tl-sm border border-white/8 bg-black/20"
        }`}
      >
        <div className="whitespace-pre-wrap text-sm leading-6 text-slate-200">
          {message.content}
        </div>

        <div className="mt-2 flex items-center gap-2 text-[10px] text-slate-600">
          <Clock3 size={11} />
          {formatTime(message.created_at)}
        </div>
      </div>

      {isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04]">
          <UserRound size={17} className="text-slate-400" />
        </div>
      )}
    </div>
  );
}

function InsightCard({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: string;
  icon: typeof Smile;
}) {
  return (
    <div className="rounded-2xl border border-white/8 bg-black/15 p-4">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-[10px] uppercase tracking-[0.16em] text-slate-500">
          {label}
        </span>

        <Icon size={16} className="text-cyan-300" />
      </div>

      <div className="truncate text-sm font-semibold text-white">
        {value}
      </div>
    </div>
  );
}

export default function GymBuddyPage() {
  const router = useRouter();

  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(
    null,
  );

  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [selectedSessionId, setSelectedSessionId] = useState<number | null>(
    null,
  );
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const [message, setMessage] = useState("");
  const [latestAnalysis, setLatestAnalysis] =
    useState<GymBuddyChatResponse | null>(null);

  const [loading, setLoading] = useState(true);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [sending, setSending] = useState(false);
  const [creatingSession, setCreatingSession] = useState(false);
  const [deletingSessionId, setDeletingSessionId] =
    useState<number | null>(null);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const selectedSession = useMemo(
    () =>
      sessions.find(
        (session) => session.id === selectedSessionId,
      ) ?? null,
    [sessions, selectedSessionId],
  );

  useEffect(() => {
    let cancelled = false;

    async function loadInitialData() {
      try {
        setLoading(true);

        const user = await getCurrentUser();

        if (cancelled) {
          return;
        }

        setCurrentUser(user);

        const sessionResponse = await getGymBuddySessions();

        if (cancelled) {
          return;
        }

        setSessions(sessionResponse.items);

        if (sessionResponse.items.length > 0) {
          const firstSession = sessionResponse.items[0];

          setSelectedSessionId(firstSession.id);

          const history = await getGymBuddySessionHistory(
            firstSession.id,
          );

          if (cancelled) {
            return;
          }

          setMessages(history.messages);
        }
      } catch (requestError) {
        if (cancelled) {
          return;
        }

        const messageText =
          requestError instanceof Error
            ? requestError.message
            : "Unable to load Gym Buddy.";

        if (
          messageText.includes("401") ||
          messageText.toLowerCase().includes("authentication")
        ) {
          router.replace("/login");
          return;
        }

        setError(messageText);
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadInitialData();

    return () => {
      cancelled = true;
    };
  }, [router]);

  function clearMessages() {
    setError("");
    setSuccess("");
  }

  async function selectSession(sessionId: number) {
    clearMessages();
    setSelectedSessionId(sessionId);

    try {
      setLoadingHistory(true);

      const history = await getGymBuddySessionHistory(sessionId);

      setMessages(history.messages);
      setLatestAnalysis(null);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to load this conversation.",
      );
    } finally {
      setLoadingHistory(false);
    }
  }

  async function handleCreateSession() {
    clearMessages();

    try {
      setCreatingSession(true);

      const session = await createGymBuddySession(
        "Gym Buddy Conversation",
      );

      setSessions((current) => [session, ...current]);
      setSelectedSessionId(session.id);
      setMessages([]);
      setLatestAnalysis(null);
      setSuccess("New Gym Buddy conversation created.");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to create a new conversation.",
      );
    } finally {
      setCreatingSession(false);
    }
  }

  async function handleDeleteSession(
    event: React.MouseEvent,
    sessionId: number,
  ) {
    event.stopPropagation();
    clearMessages();

    try {
      setDeletingSessionId(sessionId);

      await deleteGymBuddySession(sessionId);

      const remainingSessions = sessions.filter(
        (session) => session.id !== sessionId,
      );

      setSessions(remainingSessions);

      if (selectedSessionId === sessionId) {
        if (remainingSessions.length > 0) {
          const nextSession = remainingSessions[0];

          setSelectedSessionId(nextSession.id);

          const history = await getGymBuddySessionHistory(
            nextSession.id,
          );

          setMessages(history.messages);
        } else {
          setSelectedSessionId(null);
          setMessages([]);
        }

        setLatestAnalysis(null);
      }

      setSuccess("Conversation deleted.");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to delete the conversation.",
      );
    } finally {
      setDeletingSessionId(null);
    }
  }

  async function refreshSessions() {
    try {
      setLoadingHistory(true);

      const response = await getGymBuddySessions();

      setSessions(response.items);

      if (
        selectedSessionId !== null &&
        !response.items.some(
          (session) => session.id === selectedSessionId,
        )
      ) {
        setSelectedSessionId(
          response.items.length > 0
            ? response.items[0].id
            : null,
        );
      }
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to refresh conversations.",
      );
    } finally {
      setLoadingHistory(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    clearMessages();

    const trimmedMessage = message.trim();

    if (!trimmedMessage) {
      setError("Enter a message before sending.");
      return;
    }

    try {
      setSending(true);

      const response = await sendGymBuddyMessage({
        message: trimmedMessage,
        session_id: selectedSessionId,
      });

      setSelectedSessionId(response.session_id);
      setLatestAnalysis(response);

      setMessage("");

      const history = await getGymBuddySessionHistory(
        response.session_id,
      );

      setMessages(history.messages);

      const sessionResponse = await getGymBuddySessions();
      setSessions(sessionResponse.items);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Unable to send your message.",
      );
    } finally {
      setSending(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-[#050816] text-white">
        <div className="flex min-h-screen items-center justify-center">
          <div className="flex items-center gap-3 text-slate-300">
            <Loader2 className="animate-spin" size={22} />
            Loading your Gym Buddy...
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#050816] text-white">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-[8%] top-[-10%] h-[420px] w-[420px] rounded-full bg-cyan-400/[0.055] blur-[130px]" />
        <div className="absolute right-[-8%] top-[25%] h-[500px] w-[500px] rounded-full bg-blue-500/[0.055] blur-[150px]" />
        <div className="absolute bottom-[-12%] left-[35%] h-[400px] w-[400px] rounded-full bg-purple-500/[0.035] blur-[140px]" />
      </div>

      <div className="relative mx-auto max-w-[1600px] px-5 py-6 sm:px-8 lg:px-10">
        <header className="mb-6 flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
          <div>
            <div className="mb-3 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.2em] text-cyan-300">
              <Sparkles size={14} />
              Emotional Fitness Intelligence
            </div>

            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
              AI Gym Buddy
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400 sm:text-base">
              A conversational fitness companion that analyzes sentiment,
              emotion, motivation, and conversation context while keeping
              your gym conversations organized.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => router.push("/dashboard")}
              className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.035] px-4 py-2 text-xs text-slate-300 transition hover:border-cyan-400/20 hover:text-white"
            >
              <ChevronLeft size={15} />
              Dashboard
            </button>

            <div className="flex items-center gap-2 rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-xs text-emerald-300">
              <CheckCircle2 size={15} />
              AI Buddy Online
            </div>
          </div>
        </header>

        {error && (
          <div className="mb-5 flex items-start gap-3 rounded-2xl border border-rose-400/20 bg-rose-400/[0.07] px-4 py-3 text-sm text-rose-200">
            <XCircle size={18} className="mt-0.5 shrink-0" />
            {error}
          </div>
        )}

        {success && (
          <div className="mb-5 flex items-start gap-3 rounded-2xl border border-emerald-400/20 bg-emerald-400/[0.07] px-4 py-3 text-sm text-emerald-200">
            <CheckCircle2 size={18} className="mt-0.5 shrink-0" />
            {success}
          </div>
        )}

        <div className="grid min-h-[calc(100vh-220px)] gap-5 xl:grid-cols-[280px_minmax(0,1fr)_310px]">
          <aside className="rounded-3xl border border-white/10 bg-white/[0.03] p-4">
            <div className="mb-4 flex items-center justify-between">
              <div>
                <div className="text-xs uppercase tracking-[0.18em] text-slate-500">
                  Conversations
                </div>
                <div className="mt-1 text-sm font-medium text-white">
                  {sessions.length} saved
                </div>
              </div>

              <button
                type="button"
                onClick={refreshSessions}
                disabled={loadingHistory}
                className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] text-slate-400 transition hover:text-white disabled:opacity-50"
                aria-label="Refresh conversations"
              >
                <RefreshCw
                  size={15}
                  className={loadingHistory ? "animate-spin" : ""}
                />
              </button>
            </div>

            <button
              type="button"
              onClick={handleCreateSession}
              disabled={creatingSession}
              className="mb-4 flex w-full items-center justify-center gap-2 rounded-xl bg-cyan-400 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:opacity-60"
            >
              {creatingSession ? (
                <Loader2 className="animate-spin" size={16} />
              ) : (
                <Plus size={16} />
              )}
              New Conversation
            </button>

            <div className="space-y-2">
              {sessions.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-white/10 p-5 text-center">
                  <History
                    size={24}
                    className="mx-auto text-slate-600"
                  />
                  <p className="mt-3 text-xs leading-5 text-slate-500">
                    No conversations yet.
                  </p>
                </div>
              ) : (
                sessions.map((session) => (
                  <button
                    key={session.id}
                    type="button"
                    onClick={() => selectSession(session.id)}
                    className={`group flex w-full items-center gap-3 rounded-xl border p-3 text-left transition ${
                      selectedSessionId === session.id
                        ? "border-cyan-400/20 bg-cyan-400/[0.07]"
                        : "border-white/6 bg-black/10 hover:border-white/12 hover:bg-white/[0.035]"
                    }`}
                  >
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-cyan-400/10 bg-cyan-400/[0.05]">
                      <MessageCircle
                        size={15}
                        className={
                          selectedSessionId === session.id
                            ? "text-cyan-300"
                            : "text-slate-500"
                        }
                      />
                    </div>

                    <div className="min-w-0 flex-1">
                      <div className="truncate text-xs font-medium text-white">
                        {session.title || "Gym Buddy Chat"}
                      </div>
                      <div className="mt-1 text-[10px] text-slate-600">
                        {formatDate(session.updated_at)}
                      </div>
                    </div>

                    <span
                      role="button"
                      tabIndex={0}
                      aria-label="Delete conversation"
                      onClick={(event) =>
                        handleDeleteSession(event, session.id)
                      }
                      onKeyDown={(event) => {
                        if (
                          event.key === "Enter" ||
                          event.key === " "
                        ) {
                          event.preventDefault();
                          void handleDeleteSession(
                            event as unknown as React.MouseEvent,
                            session.id,
                          );
                        }
                      }}
                      className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-slate-600 opacity-0 transition hover:bg-rose-400/10 hover:text-rose-300 group-hover:opacity-100"
                    >
                      {deletingSessionId === session.id ? (
                        <Loader2
                          size={14}
                          className="animate-spin"
                        />
                      ) : (
                        <Trash2 size={14} />
                      )}
                    </span>
                  </button>
                ))
              )}
            </div>
          </aside>

          <section className="flex min-h-0 flex-col overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">
            <div className="border-b border-white/8 bg-gradient-to-r from-cyan-400/[0.06] to-blue-500/[0.025] p-5">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex min-w-0 items-center gap-4">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-cyan-400/20 bg-cyan-400/10">
                    <Bot size={22} className="text-cyan-300" />
                  </div>

                  <div className="min-w-0">
                    <div className="truncate text-sm font-semibold text-white">
                      {selectedSession?.title || "AI Gym Buddy"}
                    </div>

                    <div className="mt-1 flex items-center gap-2 text-xs text-slate-500">
                      <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
                      Your conversational fitness companion
                    </div>
                  </div>
                </div>

                <p className="rounded-xl border border-cyan-400/15 bg-cyan-400/[0.06] px-3 py-2 text-xs text-cyan-100">
                  Using your saved fitness profile
                </p>
              </div>
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto p-5">
              {loadingHistory ? (
                <div className="flex min-h-[430px] items-center justify-center">
                  <div className="flex items-center gap-3 text-sm text-slate-400">
                    <Loader2
                      size={18}
                      className="animate-spin"
                    />
                    Loading conversation...
                  </div>
                </div>
              ) : messages.length === 0 ? (
                <div className="flex min-h-[430px] flex-col items-center justify-center text-center">
                  <div className="flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-400/15 bg-cyan-400/10">
                    <Heart
                      size={28}
                      className="text-cyan-300"
                    />
                  </div>

                  <h2 className="mt-5 text-xl font-semibold">
                    Your Gym Buddy is ready
                  </h2>

                  <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
                    Start a conversation about your fitness journey,
                    motivation, gym mindset, or anything you need help
                    thinking through.
                  </p>

                  <div className="mt-6 flex flex-wrap justify-center gap-2">
                    {[
                      "I need motivation",
                      "I feel stressed",
                      "Help me stay consistent",
                    ].map((suggestion) => (
                      <button
                        key={suggestion}
                        type="button"
                        onClick={() => setMessage(suggestion)}
                        className="rounded-full border border-white/8 bg-white/[0.03] px-4 py-2 text-xs text-slate-400 transition hover:border-cyan-400/20 hover:text-cyan-300"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="space-y-5">
                  {messages.map((chatMessage) => (
                    <MessageBubble
                      key={chatMessage.id}
                      message={chatMessage}
                    />
                  ))}
                </div>
              )}
            </div>

            <div className="border-t border-white/8 p-4">
              <form
                onSubmit={handleSubmit}
                className="flex items-end gap-3"
              >
                <textarea
                  value={message}
                  onChange={(event) =>
                    setMessage(event.target.value.slice(0, 2000))
                  }
                  placeholder="Talk to your Gym Buddy..."
                  rows={2}
                  className="min-h-[52px] flex-1 resize-none rounded-2xl border border-white/10 bg-black/20 px-4 py-3 text-sm leading-6 text-white outline-none placeholder:text-slate-600 focus:border-cyan-400/35"
                />

                <button
                  type="submit"
                  disabled={sending || !message.trim()}
                  className="flex h-[52px] w-[52px] shrink-0 items-center justify-center rounded-2xl bg-cyan-400 text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
                  aria-label="Send message"
                >
                  {sending ? (
                    <Loader2
                      size={18}
                      className="animate-spin"
                    />
                  ) : (
                    <Send size={18} />
                  )}
                </button>
              </form>

              <div className="mt-2 flex items-center justify-between text-[10px] text-slate-600">
                <span>{message.length}/2000 characters</span>
                <span>
                  {currentUser?.email
                    ? `Signed in as ${currentUser.email}`
                    : "Powered by Gym Buddy + Dietician AI"}
                </span>
              </div>
            </div>
          </section>

          <aside className="space-y-5">
            <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
              <div className="mb-5 flex items-center justify-between">
                <div>
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-500">
                    AI analysis
                  </div>
                  <h2 className="mt-1 text-lg font-semibold">
                    Emotional State
                  </h2>
                </div>

                <Activity
                  size={21}
                  className="text-cyan-300"
                />
              </div>

              {!latestAnalysis ? (
                <div className="rounded-2xl border border-dashed border-white/10 p-5 text-center">
                  <Smile
                    size={26}
                    className="mx-auto text-slate-600"
                  />
                  <p className="mt-3 text-xs leading-5 text-slate-500">
                    Send a message to see the AI&apos;s sentiment,
                    emotion, motivation, and response strategy analysis.
                  </p>
                </div>
              ) : (
                <div className="grid gap-3">
                  <InsightCard
                    label="Sentiment"
                    value={labelText(
                      latestAnalysis.sentiment,
                    )}
                    icon={Smile}
                  />

                  <InsightCard
                    label="Emotion"
                    value={labelText(
                      latestAnalysis.emotion,
                    )}
                    icon={Heart}
                  />

                  <InsightCard
                    label="Motivation"
                    value={labelText(
                      latestAnalysis.motivation_level,
                    )}
                    icon={Activity}
                  />

                  <InsightCard
                    label="Intent"
                    value={labelText(latestAnalysis.intent)}
                    icon={MessageCircle}
                  />

                  <InsightCard
                    label="Strategy"
                    value={labelText(
                      latestAnalysis.strategy,
                    )}
                    icon={Sparkles}
                  />
                </div>
              )}
            </section>

            {latestAnalysis && (
              <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <div className="text-xs uppercase tracking-[0.18em] text-slate-500">
                      Confidence
                    </div>
                    <h2 className="mt-1 text-lg font-semibold">
                      Emotion Detection
                    </h2>
                  </div>

                  <Activity
                    size={20}
                    className="text-cyan-300"
                  />
                </div>

                <div className="rounded-2xl border border-cyan-400/15 bg-cyan-400/[0.05] p-5">
                  <div className="flex items-end justify-between">
                    <div>
                      <div className="text-3xl font-semibold text-white">
                        {latestAnalysis.emotion_confidence !==
                        null
                          ? `${Math.round(
                              latestAnalysis.emotion_confidence *
                                100,
                            )}%`
                          : "--"}
                      </div>
                      <div className="mt-1 text-xs text-slate-500">
                        Model confidence
                      </div>
                    </div>

                    <CheckCircle2
                      size={25}
                      className="text-emerald-300"
                    />
                  </div>

                  <div className="mt-4 h-2 overflow-hidden rounded-full bg-white/5">
                    <div
                      className="h-full rounded-full bg-cyan-400 transition-all"
                      style={{
                        width: `${
                          latestAnalysis.emotion_confidence !==
                          null
                            ? Math.max(
                                0,
                                Math.min(
                                  100,
                                  latestAnalysis.emotion_confidence *
                                    100,
                                ),
                              )
                            : 0
                        }%`,
                      }}
                    />
                  </div>
                </div>
              </section>
            )}

            {latestAnalysis?.strategy && (
              <section
                className={`rounded-3xl border p-5 ${getMetricTone(
                  latestAnalysis.strategy,
                )}`}
              >
                <div className="flex items-start gap-3">
                  <Sparkles size={19} className="mt-0.5 shrink-0" />

                  <div>
                    <div className="text-xs font-medium uppercase tracking-wide opacity-70">
                      Current AI strategy
                    </div>

                    <div className="mt-1 text-sm font-semibold">
                      {labelText(latestAnalysis.strategy)}
                    </div>

                    <p className="mt-2 text-xs leading-5 opacity-70">
                      The response strategy is selected from the
                      conversation analysis returned by the backend.
                    </p>
                  </div>
                </div>
              </section>
            )}
          </aside>
        </div>
      </div>
    </main>
  );
}
