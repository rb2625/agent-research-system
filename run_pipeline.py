import sys
from app.config import settings
from app.orchestrator import run_research


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py \"your topic here\"")
        sys.exit(1)

    settings.validate()

    topic = " ".join(sys.argv[1:])
    print(f"Topic: {topic}\n")

    result = run_research(topic)

    print("Subtasks:")
    for subtask in result["subtasks"]:
        print(f"  - {subtask}")

    print(f"\nReport:\n{result['report']}")


if __name__ == "__main__":
    main()