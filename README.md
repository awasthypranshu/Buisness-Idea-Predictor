# 💡 Business Idea Predictor & Generator

An AI-powered SaaS web application that generates, analyzes, and predicts innovative business ideas with a focus on autonomous AI agents. Built with a **Next.js 16** frontend and a high-performance **FastAPI** backend, featuring real-time Server-Sent Events (SSE) streaming powered by **Groq Cloud**.

---

## 🚀 Features

- **⚡ Real-Time Token Streaming**: Streams generated business ideas token-by-token using Server-Sent Events (`EventSource` + `StreamingResponse`), delivering instant feedback without loading freezes.
- **🧠 Ultra-Fast Groq Inference**: Powered by Groq's high-throughput LPU inference running state-of-the-art open models (`openai/gpt-oss-120b`).
- **📝 Formatted Markdown Presentation**: Full GitHub Flavored Markdown (GFM) rendering with `react-markdown`, `remark-gfm`, and `remark-breaks` for structured headings, bullet points, and roadmaps.
- **🎨 Modern Glassmorphic UI**: Sleek, responsive card design styled with Tailwind CSS v4, supporting dynamic dark and light mode aesthetics.
- **☁️ Serverless-Ready Architecture**: Built to deploy seamlessly on Vercel with zero-configuration hybrid Next.js frontend and Python serverless functions.

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
|---|---|---|
| **Frontend Framework** | [Next.js 16](https://nextjs.org/) (Pages Router) | React framework with Turbopack support |
| **UI Library** | [React 19](https://react.dev/) | Declarative modern user interface |
| **Language** | [TypeScript](https://www.typescriptlang.org/) & [Python 3.10+](https://www.python.org/) | Type-safe frontend and backend code |
| **Styling** | [Tailwind CSS v4](https://tailwindcss.com/) | Modern utility-first CSS framework |
| **Markdown** | `react-markdown` + `remark-gfm` + `remark-breaks` | Live rendering of streaming markdown text |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance Python async web framework |
| **AI Engine** | [Groq Cloud](https://groq.com/) | Ultra-low latency LLM inference via OpenAI SDK |
| **Deployment** | [Vercel](https://vercel.com/) | Hybrid serverless Next.js + Python deployment |

---

## 🏗️ Architecture & Data Flow

```mermaid
flowchart LR
    User([User / Browser])
    
    subgraph Frontend ["Next.js Frontend (React 19)"]
        UI["UI Card / State"]
        ES["EventSource('/api')"]
        MD["ReactMarkdown + GFM"]
    end
    
    subgraph Backend ["FastAPI Backend (/api/index.py)"]
        Endpoint["GET /api"]
        StreamGenerator["StreamingResponse (text/event-stream)"]
    end
    
    subgraph AI ["Groq Cloud Inference"]
        GroqAPI["Groq LPU Engine\n(openai/gpt-oss-120b)"]
    end
    
    User -->|Open Page| UI
    UI -->|Mount useEffect| ES
    ES -->|GET Request| Endpoint
    Endpoint -->|client.chat.completions.create(stream=True)| GroqAPI
    GroqAPI -.->|Token Chunks| StreamGenerator
    StreamGenerator -.->|SSE Events data: ...| ES
    ES -->|Incremental buffer update| MD
    MD -->|Render live idea| User
```

---

## 📁 Project Structure

```text
├── api/
│   └── index.py             # FastAPI backend with Groq streaming endpoint (/api)
├── pages/
│   ├── _app.tsx             # Global application wrapper and style imports
│   ├── _document.tsx        # HTML document structure and SEO meta tags
│   └── index.tsx            # Main page with SSE EventSource and Markdown viewer
├── public/                  # Static assets and favicons
├── styles/
│   └── globals.css          # Tailwind CSS v4 imports and custom markdown styles
├── .env.example             # Example environment variables template
├── .gitignore               # Git ignore rules for Next.js, Python, and secrets
├── next.config.ts           # Next.js and Turbopack configuration
├── package.json             # Frontend dependencies and npm scripts
├── requirements.txt         # Python dependencies for FastAPI backend
└── tsconfig.json            # TypeScript configuration
```

---

## ⚙️ Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- **Node.js** 18.x or higher
- **npm**, **pnpm**, or **yarn**
- **Python** 3.10 or higher
- A **Groq API Key** (Get one for free at [console.groq.com](https://console.groq.com/keys))

---

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/awasthypranshu/Buisness-Idea-Predictor.git
   cd Buisness-Idea-Predictor
   ```

2. **Install Frontend Dependencies:**
   ```bash
   npm install
   ```

3. **Install Python Dependencies:**
   ```bash
   # Create and activate a virtual environment (optional but recommended)
   python -m venv .venv

   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env.local` file in the root directory:
   ```bash
   cp .env.example .env.local
   ```
   Open `.env.local` and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_groq_api_key_here
   ```

---

### Running Locally

#### Option A: Using Vercel CLI (Recommended)
The Vercel CLI automatically runs both the Next.js frontend and the FastAPI serverless function concurrently:

```bash
# Install Vercel CLI globally (if not already installed)
npm i -g vercel

# Run the local development server with environment variables
vercel dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

#### Option B: Running Concurrently (Manual)
If you prefer running the Next.js dev server and FastAPI separately:

1. **Terminal 1 - FastAPI Server:**
   ```bash
   uvicorn api.index:app --reload --port 8000
   ```
2. **Terminal 2 - Next.js Development Server:**
   ```bash
   npm run dev
   ```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | **Yes** | Your API key from Groq Cloud used to authenticate completions requests. |

---

## 📡 API Reference

### `GET /api`

Generates and streams an AI-agent business proposal using Server-Sent Events (SSE).

- **Request Headers**: `Accept: text/event-stream`
- **Response Headers**: 
  - `Content-Type: text/event-stream`
  - `Cache-Control: no-cache`
- **Response Format**:
  ```text
  data: ## Autonomous Quality Assurance Agent
  
  data: ### Executive Summary
  
  data: - Automated end-to-end testing platform
  data: - Adapts to UI changes dynamically
  ```

---

## 🚀 Deployment to Vercel

This repository is pre-configured for one-click deployment on [Vercel](https://vercel.com):

1. Push your repository to GitHub.
2. Go to [Vercel](https://vercel.com/new) and import the repository: `awasthypranshu/Buisness-Idea-Predictor`.
3. Under **Environment Variables**, add:
   - Key: `GROQ_API_KEY`
   - Value: `<your-groq-api-key>`
4. Click **Deploy**. Vercel will automatically build the Next.js pages and host the Python FastAPI endpoint as a Serverless Function.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
