from groq import Groq
from ..config import settings

WRITER_PROMPT = (
    "You are a research writer. You are given a topic and a set of findings "
    "gathered by separate researchers, each covering one subtask. Combine "
    "them into one clear, well-organized report. Check that claims are "
    "consistent across findings and flag anything that looks contradictory. "
    "Keep the citations from the original findings."
)


def write_report(topic: str, findings: list, model: str = None) -> str:
    client = Groq(api_key=settings.groq_api_key)

    findings_text = "\n\n".join(
        f"Subtask: {item['subtask']}\nFindings: {item['findings']}"
        for item in findings
    )

    response = client.chat.completions.create(
        model=model or settings.model,
        messages=[
            {"role": "system", "content": WRITER_PROMPT},
            {"role": "user", "content": f"Topic: {topic}\n\n{findings_text}"},
        ],
    )

    return response.choices[0].message.content