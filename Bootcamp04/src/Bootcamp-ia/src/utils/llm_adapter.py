import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def get_llm():
    """
    Instancia e retorna o LLM base. 
    A temperatura 0 é ideal aqui para garantir respostas determinísticas 
    ao aplicar as regras de negócio de navegação.
    """
    return ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0        
    )