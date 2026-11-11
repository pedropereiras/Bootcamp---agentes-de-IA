import os
from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Variável de ambiente '{name}' ausente. "
            "Defina a chave correta no arquivo .env ou no ambiente antes de executar o projeto."
        )
    return value


def get_llm():
    """
    Instancia e retorna o LLM conforme o provedor configurado no ambiente.
    A temperatura 0 é ideal aqui para garantir respostas determinísticas
    ao aplicar as regras de negócio de navegação.
    """
    provider = os.getenv("LLM_PROVIDER")
    model = os.getenv("LLM_MODEL")

    if provider == "groq":
        try:
            from langchain_groq import ChatGroq
        except ImportError as exc:
            raise RuntimeError(
                "O pacote 'langchain-groq' não está instalado. "
                "Adicione 'langchain-groq' ao requirements.txt e instale as dependências."
            ) from exc

        return ChatGroq(
            model=model or "openai/gpt-oss-120b", 
            api_key=_require_env("GROQ_API_KEY"),
            temperature=0,
        )
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=model or "gpt-4o-mini",
            api_key=_require_env("OPENAI_API_KEY"),
            temperature=0,
        )

    raise ValueError(f"Provedor de LLM não suportado: '{provider}'.")

