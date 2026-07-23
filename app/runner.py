from .agent import Agent
from .providers.gemini_agent import GeminiAgent
from .cache import SemanticCache
from .config import settings

_cache = SemanticCache()


def run_task(task: str, system_prompt: str = None) -> dict:
    cached = _cache.get(task)
    if cached is not None:
        result = dict(cached)
        result["from_cache"] = True
        return result

    result = None
    errors = []

    try:
        agent = Agent(system_prompt=system_prompt)
        result = agent.run(task)
        result["provider"] = "groq"
    except Exception as error:
        errors.append(f"groq failed: {error}")

        if settings.gemini_api_key:
            try:
                agent = GeminiAgent(system_prompt=system_prompt)
                result = agent.run(task)
                result["provider"] = "gemini"
            except Exception as fallback_error:
                errors.append(f"gemini failed: {fallback_error}")

    if result is None:
        raise RuntimeError("All providers failed.\n" + "\n".join(errors))

    result["from_cache"] = False
    _cache.set(task, result)
    return result