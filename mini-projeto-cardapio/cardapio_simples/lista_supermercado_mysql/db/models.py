"""Modelos usados para a criação das tabelas no banco de dados"""

# Bibliotecas
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

# quando for executar o servidor
try:
    from db.database import Base
    
# quando for executar os testes
except ImportError:
    from lista_supermercado_mysql.db.database import Base

class Produto(Base):
    __tablename__ = "produto"
    
    id: int = Column(Integer, primary_key=True, index=True)
    item: str = Column(String(100), nullable=False)
    quantidade: int = Column(Integer, nullable=False)
    preco: float = Column(Float, nullable=True)
    tipo: str = Column(String(50), nullable=False)
     
    
class Pedido(Base):
    __tablename__ = "pedido"
    
    id: int = Column(Integer, primary_key=True, index=True)
    preco: float = Column(Float, nullable=True)
    produtos: str = Column(String(500), nullable=False)
    
