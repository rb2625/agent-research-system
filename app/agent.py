import json
from groq import Groq
from .config import settings
from .tools import TOOL_SPECS, TOOL_FUNCTIONS

DEFAULT_SYSTEM_PROMPT = (
    "You are a research assistant. Use the search_web tool to gather current, "
    "accurate information before answering. Cite the sources you used by "
    "referencing their URLs. If the question can be answered without a search, "
    "you may answer directly."
)


class Agent:
    def __init__(self, model: str = None, max_iterations: int = None, system_prompt: str = None):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = model or settings.model
        self.max_iterations = max_iterations or settings.max_iterations
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    def run(self, task: str) -> dict:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task},
        ]
        tool_calls_made = []

        for iteration in range(self.max_iterations):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOL_SPECS,
            )

            message = response.choices[0].message

            if not message.tool_calls:
                return {
                    "answer": message.content or "",
                    "iterations": iteration + 1,
                    "tool_calls": tool_calls_made,
                }

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": message.tool_calls,
            })

            for call in message.tool_calls:
                tool_name = call.function.name
                tool_input = json.loads(call.function.arguments)
                tool_calls_made.append({"tool": tool_name, "input": tool_input})

                function = TOOL_FUNCTIONS.get(tool_name)
                if function is None:
                    result_text = f"Unknown tool: {tool_name}"
                else:
                    result_text = function(**tool_input)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result_text,
                })

        return {
            "answer": "Reached the maximum number of iterations without a final answer.",
            "iterations": self.max_iterations,
            "tool_calls": tool_calls_made,
        }