from src.graph.builder import build_graph

NAVIOS = ["S1-FAROL", "S2-MARE", "S3-CORAL", "S4-FAROL", "S5-MARE", "S6-CORAL"]

def main() -> None:
    graph = build_graph()
    
    for ship_id in NAVIOS:
        print(f"--- Iniciando processamento do navio: {ship_id} ---")
        try:
            # Injetamos o estado inicial contendo apenas o ID do navio
            saida = graph.invoke({"ship_id": ship_id})
            
            # Usamos .get() por segurança caso o estado falhe no meio e não gere a chave 'resultado'
            resultado = saida.get("resultado", "Processamento concluído, mas sem resultado final.")
            print(f"Sucesso [{ship_id}]: {resultado}\n")
            
        except Exception as e:
            # Captura a falha específica deste navio, exibe o erro real e permite que o loop continue
            print(f"Falha ao processar o navio {ship_id}: {type(e).__name__} - {e}\n")
            continue

if __name__ == "__main__":
    main()