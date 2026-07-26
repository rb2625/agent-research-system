from concurrent.futures import ThreadPoolExecutor, as_completed
from .agents.planner import create_plan
from .agents.researcher import research_subtask
from .agents.writer import write_report


def run_research(topic: str, on_step=None) -> dict:
    def emit(message):
        if on_step:
            on_step(message)

    emit("Planning research")
    subtasks = create_plan(topic)
    emit(f"Planner split the topic into {len(subtasks)} subtasks")

    findings = []
    with ThreadPoolExecutor(max_workers=len(subtasks)) as executor:
        future_to_subtask = {
            executor.submit(research_subtask, subtask): subtask
            for subtask in subtasks
        }
        for future in as_completed(future_to_subtask):
            result = future.result()
            findings.append(result)
            emit(f"Researcher finished: {result['subtask']}")

    emit("Writing final report")
    report = write_report(topic, findings)
    emit("Report complete")

    return {
        "topic": topic,
        "subtasks": subtasks,
        "findings": findings,
        "report": report,
    }