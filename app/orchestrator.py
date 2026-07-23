from concurrent.futures import ThreadPoolExecutor
from .agents.planner import create_plan
from .agents.researcher import research_subtask
from .agents.writer import write_report


def run_research(topic: str) -> dict:
    subtasks = create_plan(topic)

    with ThreadPoolExecutor(max_workers=len(subtasks)) as executor:
        findings = list(executor.map(research_subtask, subtasks))

    report = write_report(topic, findings)

    return {
        "topic": topic,
        "subtasks": subtasks,
        "findings": findings,
        "report": report,
    }