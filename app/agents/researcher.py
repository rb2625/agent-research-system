from ..agent import Agent

RESEARCHER_PROMPT = (
    "You are a research agent. Use the search_web tool to investigate the "
    "subtask you are given. Write a concise, factual summary of what you "
    "found, and list the source URLs you used."
)


def research_subtask(subtask: str) -> dict:
    agent = Agent(system_prompt=RESEARCHER_PROMPT)
    result = agent.run(subtask)
    return {
        "subtask": subtask,
        "findings": result["answer"],
        "tool_calls": result["tool_calls"],
    }