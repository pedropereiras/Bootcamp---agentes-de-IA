# Despachante do porto

## Configuração

Instale as dependências com `pip install -r requirements.txt`, copie `.env.example` para `.env` e configure `GROQ_API_KEY` (ou `LLM_PROVIDER=openai` e `OPENAI_API_KEY`).

## Execução

Na raiz do projeto: `python -m src.app.main`.

Para executar o exercício 1, use `python -c "from src.graph.builder_exercise1 import build_graph; print(build_graph().invoke({'pergunta':'Qual navio chega primeiro?'})['resultado'])"`. Para testar o prompt de uma linha, em `src/graph/nodes/decide.py`, troque `PROMPT = PROMPT_MELHORADO` por `PROMPT = PROMPT_UMA_LINHA`; restaure o melhorado para os testes seguintes.
