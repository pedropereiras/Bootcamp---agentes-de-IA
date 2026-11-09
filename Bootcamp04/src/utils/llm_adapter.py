import os

from dotenv import load_dotenv

load_dotenv()


def get_llm():
    """Cria o chat model a partir das variáveis de ambiente configuradas."""
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    model = os.getenv("LLM_MODEL")
    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(model=model or "openai/gpt-oss-120b", temperature=0)
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model or "gpt-4o-mini", temperature=0)
    raise ValueError("LLM_PROVIDER deve ser 'groq' ou 'openai'.")
