# Agent Research System

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Next.js](https://img.shields.io/badge/next.js-14-black)

An autonomous multi-agent research system. Give it a topic, and a team of AI agents plans it, researches it in parallel, and writes a cited report backed by a reliability layer that keeps it working even when a provider rate-limits or fails.

## How it works

1. **Planner agent** breaks a topic into 2-3 focused subtasks
2. **Researcher agents** investigate each subtask in parallel, using a web search tool
3. **Writer agent** combines all findings into one coherent, cited report and checks for contradictions across sources

Underneath, every LLM call goes through:

- A **semantic cache** (TF-IDF based) that skips duplicate or near-duplicate questions
- **Multi-provider fallback** if Groq fails or rate-limits, it automatically retries on Google Gemini
- A **rate limiter** that spaces out parallel requests so they don't trip provider limits

The whole thing runs on free infrastructure: Groq (Llama 3.3 70B) as the primary model, Gemini as fallback, Tavily for search.

## Architecture

```
Topic
  |
Planner agent -> splits into subtasks
  |
Researcher agents (parallel) -> search + summarize each subtask
  |
Writer agent -> synthesizes findings into one cited report
```

Every agent call passes through a caching + rate-limiting + fallback layer before reaching Groq or Gemini.

## Setup

Requirements: Python 3.10+, Node.js 18+, and three free API keys (no credit card required for any of them):

- [Groq](https://console.groq.com) primary model
- [Google AI Studio](https://aistudio.google.com/apikey) fallback model
- [Tavily](https://tavily.com) web search

### Backend

```
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in your three API keys in `.env`, then start the server:

```
python -m uvicorn app.main:app --reload
```

### Frontend

In a separate terminal:

```
cd backend/frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

### Command-line testing (no frontend needed)

Single agent:

```
python run.py "your question here"
```

Full multi-agent pipeline:

```
python run_pipeline.py "your topic here"
```

## Project structure

```
backend/
  app/
    agent.py            single-agent reasoning loop (think, act, observe)
    agents/
      planner.py        splits a topic into subtasks
      researcher.py      researches one subtask using the agent loop
      writer.py           combines findings into a final report
    providers/
      gemini_agent.py    fallback provider implementation
    orchestrator.py      runs the full pipeline, planner -> parallel researchers -> writer
    runner.py            wraps a single agent call with caching and provider fallback
    cache.py             TF-IDF based semantic cache
    rate_limiter.py       token-bucket rate limiter, one per provider
    jobs.py               in-memory job store for tracking live progress
    main.py              FastAPI app: starts research jobs, serves live status
    tools.py              web search tool definition
    config.py             environment variable loading and validation
  run.py                  CLI entrypoint, single agent
  run_pipeline.py         CLI entrypoint, full multi-agent pipeline
  frontend/               Next.js app: input, live progress, rendered report
```

## Known limitations

- **Caching is lexical, not semantic.** It uses TF-IDF similarity, which catches close rewordings of the same question but can't recognize true synonyms (e.g. "world" vs "earth"). The threshold is set conservatively (favoring missed cache hits over incorrect ones) since a false-positive cache hit returning a cached answer for an unrelated question is a worse failure than an unnecessary API call.
- **Job progress is stored in memory.** Restarting the backend clears any in-progress or completed job history. A production version would use Redis or a database instead.
- **Rate limits are estimated**, not pulled from the provider's actual account limits. Defaults are set conservatively for free-tier usage.

## Roadmap

- ✅ Single agent with web search tool
- ✅ Multi-agent orchestration (planner, parallel researchers, writer)
- ✅ Semantic caching, multi-provider fallback, rate limiting
- ✅ Live progress tracking API
- ✅ Next.js frontend with live status and rendered reports
- ✅ Docker packaging for one-command setup
- ⬜ Persistent job storage
