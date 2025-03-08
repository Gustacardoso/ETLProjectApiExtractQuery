import time
import requests
from tinydb import TinyDB
from datetime import datetime


def extract_dados_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    dados = response.json()
    return dados

def transform_dados(dados):
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

def salvar_dados_tinydb(dados, db_name='dados_bitcoin.json'):
    db = TinyDB(db_name)
    db.insert(dados)
    print(f"Dados salvos em {db_name}")
    
if __name__ == "__main__":
    while True:
        dados_json = extract_dados_bitcoin()
        dados_tratados = transform_dados(dados_json)
        salvar_dados_tinydb(dados_tratados)
        time.sleep(15)



