import sys
from app.config import settings
from app.runner import run_task


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"your question here\"")
        sys.exit(1)

    settings.validate()

    task = " ".join(sys.argv[1:])
    print(f"Task: {task}\n")

    result = run_task(task)

    print(f"Answer:\n{result['answer']}\n")
    print(f"Completed in {result['iterations']} iteration(s), "
          f"{len(result['tool_calls'])} tool call(s) made.")
    print(f"Served from cache: {result['from_cache']}")
    if not result["from_cache"]:
        print(f"Provider used: {result.get('provider', 'unknown')}")


if __name__ == "__main__":
    main()