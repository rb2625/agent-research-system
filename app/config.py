import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY", "")
        self.model = os.getenv("AGENT_MODEL", "llama-3.3-70b-versatile")
        self.max_iterations = int(os.getenv("AGENT_MAX_ITERATIONS", "8"))

    def validate(self):
        missing = []
        if not self.groq_api_key:
            missing.append("GROQ_API_KEY")
        if not self.tavily_api_key:
            missing.append("TAVILY_API_KEY")
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Copy .env.example to .env and fill in your keys."
            )


settings = Settings()
