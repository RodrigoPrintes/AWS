"""Modelo para representar um pedido """

# Bibliotecas
from pydantic import BaseModel
from typing import Optional


#from db.repositories import ProdutoRepository, PedidoRepository

class PedidoBase(BaseModel):
    
    produtos: str 
    
    
    


class PedidoRequest(PedidoBase):
    
    ...
    
class PedidoResponse(PedidoBase):
    id : int
    preco : float
    #products : list[ProdutoRequest]

    class Config:
        orm_mode = True



