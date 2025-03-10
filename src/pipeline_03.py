import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
# Importar Base e BitcoinPreco do database.py
from database.tabela_bitcoin_precos import Base, bitcoinPreco

#carrega variaveis de ambiente do  arquivo .env
load_dotenv()

#le as variaveis sepadaradas do arquivo .env (sem SSL)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
#criar o engine e a sessão


DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def criar_tabela():
    """Criar a tabela no banco de dados, se não existe."""
    Base.metadata.create_all(engine)
    print("Tabela  criada/verificada com sucesso")

def extract_dados_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
   
    if response.status_code == 200:
         return response.json()
    else:
        print(f"Erro API: {response.status_code}")
        return None

def transform_dados_bitcon(dados):
    valor = dados['data']['amount']
    criptomoeda = dados['data']['base']
    moeda = dados['data']['currency']
    timestamp = datetime.now().isoformat()
    
    dados_transformados = {
        'valor': valor,
        'criptomoeda': criptomoeda,
        'moeda': moeda,
        'timestamp': timestamp
    }
    return dados_transformados

def salvar_dados_postgres(dados):
    """Salva os dados no banco postgreSQL."""
    session = Session()
    novo_registro = bitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    print(f"[{dados['timestamp']}] Dados salvos no PostgreSQL!")
    
if __name__ == "__main__":
   criar_tabela()
   print("Iniciando ETL com atualização a cada 15 segundos ... (CTRL+C para interromper)")
   
   while True:
       try:
           dados_json = extract_dados_bitcoin()
           if dados_json:
               dados_tratados = transform_dados_bitcon(dados_json)
               print("Dados Tratados:", dados_tratados)
               salvar_dados_postgres(dados_tratados)
           time.sleep(15)
       except KeyboardInterrupt:
           print("\Processo interrompido pelo usuario. Finalizando ...")
           break
       except Exception as e:
           print(f"Erro durante a execução: {e}")
           time.sleep(15)
              
               



