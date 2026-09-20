# AI Gym & Fitness Assistant

A unified fitness dashboard built with Next.js and FastAPI. It combines AI workout analysis, nutrition coaching, habit insights, Smart Gym telemetry, a motivational chat companion, and personalized fitness recommendations.

## Current feature coverage

- One-time fitness setup: new users select their goal, food preference, activity level, training location, and body metrics once. These values are saved in the account, can be edited in Profile, and are not requested again by Dietician or Gym Buddy.
- My Plan: gives each signed-in user a goal-based daily workout plan for home or gym training plus a personalized diet plan generated from the saved profile.
- AI Trainer: upload a workout video for rep-level form and performance analysis, or use the Live AI Trainer camera session for real-time squat counting, a visual squat movement guide, and spoken coaching. The AI Buddy creates a daily goal-, activity-, and training-setting-aware workout focus and warm-up checklist. Live camera frames are processed without being stored.
- Dietician and Calorie Coach: calculate nutrition targets, create meal plans, log food, and use the diet chat without re-entering profile details.
- Gym Buddy: conversational motivation with sentiment and emotion signals.
- Habit Tracker: predicts workout-skip risk and recommends the next session.
- Pose-to-Performance: shows recent analysis history and weekly form-quality scores.
- Smart Gym: displays IoT equipment telemetry and the latest AI control action.
- Fitness Planner: generates gym, workout-program, and challenge recommendations.
- Analytics and Admin: shows workout, nutrition, recovery, and system metrics.
- Public website: visitors can explore the home page, how-it-works guide, diet-plan overview, and developer profile before signing in.
- Account access: user registration, separate user and administrator sign-in, and an administrator user directory with account-status controls.
- Persistent navigation and contact details: the workspace sidebar stays visible on desktop pages, while the site footer shows developer contact details across the application.

## Run locally

1. Configure the required backend environment values in `backend/.env` (database URL and JWT secret are required).
2. Install the backend dependencies from `requirements.txt` in a working Python 3.11+ environment.
3. From `backend`, start the API with `uvicorn app.main:app --port 8001`.
4. From `frontend`, install the Node dependencies and run `npm run dev`.
5. Open `http://localhost:3000`.

For richer free-form Dietician conversations, add an OpenAI API key only to your own local `backend/.env` file as `OPENAI_API_KEY=...`, then restart the backend. Do not commit or send an API key in chat. The live squat camera coach and its spoken cues work locally without an OpenAI key.

The local frontend configuration proxies API requests to `http://localhost:8001/api/v1`. If the API is unavailable, every data-driven page shows a clear “backend API is offline” message and its retry control remains usable.

## Frontend checks

From `frontend`:

```text
npm run lint
npm run build
```
