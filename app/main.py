import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import settings
from .orchestrator import run_research
from . import jobs

app = FastAPI(title="Agent Research System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str


@app.on_event("startup")
def startup():
    settings.validate()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def start_research(request: ResearchRequest):
    job_id = jobs.create_job()

    def run():
        try:
            def on_step(message):
                jobs.add_step(job_id, message)

            result = run_research(request.topic, on_step=on_step)
            jobs.complete_job(job_id, result)
        except Exception as error:
            jobs.fail_job(job_id, str(error))

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    return {"job_id": job_id}


@app.get("/research/{job_id}")
def get_research(job_id: str):
    job = jobs.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job