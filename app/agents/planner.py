import json
from groq import Groq
from ..config import settings

PLANNER_PROMPT = (
    "You are a research planner. Given a topic, break it down into 2 to 3 "
    "specific, non-overlapping subtasks that together cover the topic well. "
    "Respond with only a JSON array of strings, no other text. "
    "Example: [\"subtask one\", \"subtask two\", \"subtask three\"]"
)


def create_plan(topic: str, model: str = None) -> list:
    client = Groq(api_key=settings.groq_api_key)
    response = client.chat.completions.create(
        model=model or settings.model,
        messages=[
            {"role": "system", "content": PLANNER_PROMPT},
            {"role": "user", "content": topic},
        ],
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        subtasks = json.loads(raw)
    except json.JSONDecodeError:
        subtasks = [topic]

    if not isinstance(subtasks, list) or not subtasks:
        subtasks = [topic]

    return subtasks[:3]