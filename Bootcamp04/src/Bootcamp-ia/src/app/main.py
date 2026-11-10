from src.graph.builder import build_graph
# Importe a configuração do seu observador (ex: Langfuse), se estiver utilizando
from src.utils.langfuse_client import flush, run_config 

NAVIOS = ["S1-FAROL", "S2-MARE", "S3-CORAL"]

def main() -> None:
    graph = build_graph()
    
    for ship_id in NAVIOS:
        # Injetamos o estado inicial contendo apenas o ID do navio
        saida = graph.invoke({"ship_id": ship_id}, run_config=run_config())
        print(saida["resultado"])
        
    flush()

if __name__ == "__main__":
    main()