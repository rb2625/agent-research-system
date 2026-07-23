from google import genai
from google.genai import types
from ..config import settings
from ..tools import TOOL_FUNCTIONS

DEFAULT_SYSTEM_PROMPT = (
    "You are a research assistant. Use the search_web tool to gather current, "
    "accurate information before answering. Cite the sources you used by "
    "referencing their URLs. If the question can be answered without a search, "
    "you may answer directly."
)

SEARCH_TOOL = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="search_web",
        description=(
            "Search the web for current information on a topic. "
            "Returns a list of sources with titles, URLs, and short summaries."
        ),
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query."},
                "max_results": {"type": "integer", "description": "Number of results to return, default 5."},
            },
            "required": ["query"],
        },
    )
])


class GeminiAgent:
    def __init__(self, model: str = None, max_iterations: int = None, system_prompt: str = None):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = model or settings.gemini_model
        self.max_iterations = max_iterations or settings.max_iterations
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT

    def run(self, task: str) -> dict:
        contents = [types.Content(role="user", parts=[types.Part(text=task)])]
        tool_calls_made = []

        for iteration in range(self.max_iterations):
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    tools=[SEARCH_TOOL],
                ),
            )

            candidate = response.candidates[0]
            parts = candidate.content.parts or []
            function_calls = [p for p in parts if p.function_call]

            if not function_calls:
                text = "".join(p.text or "" for p in parts)
                return {
                    "answer": text,
                    "iterations": iteration + 1,
                    "tool_calls": tool_calls_made,
                }

            contents.append(candidate.content)

            response_parts = []
            for part in function_calls:
                name = part.function_call.name
                args = dict(part.function_call.args)
                tool_calls_made.append({"tool": name, "input": args})

                function = TOOL_FUNCTIONS.get(name)
                if function is None:
                    result_text = f"Unknown tool: {name}"
                else:
                    result_text = function(**args)

                response_parts.append(
                    types.Part.from_function_response(
                        name=name,
                        response={"result": result_text},
                    )
                )

            contents.append(types.Content(role="tool", parts=response_parts))

        return {
            "answer": "Reached the maximum number of iterations without a final answer.",
            "iterations": self.max_iterations,
            "tool_calls": tool_calls_made,
        }