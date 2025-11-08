# src/main.py
from api_senado import APISenado
from processador_dados import ProcessadorDadosSenado
import pandas as pd

def main():
    api = APISenado()
    
    # Buscar senadores
    senadores = api.buscar_senadores_atuais()
    df_senadores = ProcessadorDadosSenado.senadores_para_dataframe(senadores)
    
    print(f"Encontrados {len(df_senadores)} senadores")
    df_senadores.to_csv('../data/senadores.csv', index=False)

if __name__ == "__main__":
    main()