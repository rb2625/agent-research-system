from ..runner import run_task

RESEARCHER_PROMPT = (
    "You are a research agent. Use the search_web tool to investigate the "
    "subtask you are given. Write a concise, factual summary of what you "
    "found, and list the source URLs you used."
)


def research_subtask(subtask: str) -> dict:
    result = run_task(subtask, system_prompt=RESEARCHER_PROMPT)
    return {
        "subtask": subtask,
        "findings": result["answer"],
        "tool_calls": result["tool_calls"],
        "provider": result.get("provider", "cache"),
    }