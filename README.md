
````markdown
# 📖 StoryWeaverAI

An AI-powered, interactive "Choose Your Own Adventure" story generator. Provide a theme, and let Google's Gemini AI craft a unique, branching narrative for you to explore.

![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)
![Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4?logo=google-gemini)

---

## ✨ Features

* **AI-Powered:** Generates unique, multi-path stories from any user-provided theme (e.g., "Pirates", "Cyberpunk").
* **Interactive:** Users make choices that lead to different parts of the story, with multiple winning or losing endings.
* **Asynchronous Generation:** Uses a backend job queue to handle AI generation without blocking the UI.
* **Real-Time Polling:** The frontend polls for the story status and automatically navigates when the story is ready.

---

## 🛠️ Tech Stack

* **Frontend:** React (Vite), `react-router-dom`, `axios`
* **Backend:** Python 3.11+, FastAPI, SQLAlchemy
* **Database:** PostgreSQL
* **AI:** Google Gemini (via LangChain)
* **Deployment:** Vercel (Frontend), Render (Backend), Supabase (Database)

---

## 🔧 Getting Started: Local Development

Follow these steps to run the project on your local machine.

### Prerequisites

* [Git](https://git-scm.com/)
* [Python 3.10+](https://www.python.org/downloads/)
* [Node.js (v18+)](https://nodejs.org/)
* A running PostgreSQL server (or a free Supabase account)

---

### 1. Clone the Repository

```bash
# Fix: This link is now correct
git clone [https://github.com/your-username/StoryWeaverAI.git](https://github.com/your-username/StoryWeaverAI.git)
cd StoryWeaverAI
````

-----

### 2\. Backend Setup (FastAPI)

```bash
# Navigate to the backend folder
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create your .env file
touch .env
```

Now, add your secret keys to the new `.env` file you just created:

**`/backend/.env`**

```
# Your Supabase/Postgres connection string
DATABASE_URL="postgresql://user:password@host:port/dbname"

# Your Google AI Studio API key
GEMINI_API_KEY="AIzaSy...your...key...here"

# Your frontend's local address for CORS
ALLOWED_ORIGINS="http://localhost:5173"
```

**Run the backend server:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Your backend will be running at `http://127.0.0.1:8000`.

-----

### 3\. Frontend Setup (React)

Open a **new terminal** for the frontend.

```bash
# Navigate to the frontend folder
cd frontend

# Install dependencies
npm install

# Create your development .env file
touch .env.development
```

Now, add the backend's local address to the `.env.development` file:

**`/frontend/.env.development`**

```
VITE_API_BASE_URL="[http://127.0.0.1:8000](http://127.0.0.1:8000)"
```

**Run the frontend server:**

```bash
npm run dev
```

Your frontend will be running at `http://localhost:5173`.

-----

## 📜 License

Distributed under the MIT License.

```
```
