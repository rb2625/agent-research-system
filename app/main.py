from fastapi import FastAPI
from pydantic import BaseModel
from .config import settings
from .agent import Agent

app = FastAPI(title="Agent Research System")


class ResearchRequest(BaseModel):
    task: str


class ResearchResponse(BaseModel):
    answer: str
    iterations: int
    tool_calls: list


@app.on_event("startup")
def startup():
    settings.validate()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    agent = Agent()
    result = agent.run(request.task)
    return result
