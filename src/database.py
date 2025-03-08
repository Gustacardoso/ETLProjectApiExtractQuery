from sqlalchemy.orm import declarative_base
from sqlalchemy import column, Float, String, Integer, DateTime
from datetime import datetime

#cria a classe Base do SQLALchemy(na versão 2.x)
Base = declarative_base()

class bitcoinPreco(Base):
    """define a tabela no banco de dados"""
    __tablename__ = "bitcoin_precos"
    
    id= column(Integer, primary_key= True, autoinchement=True)
    valor = column(Float)