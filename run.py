import sys
from app.config import settings
from app.agent import Agent


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"your question here\"")
        sys.exit(1)

    settings.validate()

    task = " ".join(sys.argv[1:])
    agent = Agent()

    print(f"Task: {task}\n")
    result = agent.run(task)

    print(f"Answer:\n{result['answer']}\n")
    print(f"Completed in {result['iterations']} iteration(s), "
          f"{len(result['tool_calls'])} tool call(s) made.")


if __name__ == "__main__":
    main()
