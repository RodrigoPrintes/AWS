"""Para acesso às informações contidas no banco de dados"""

# Bibliotecas
from sqlalchemy.orm import Session

try:
    from db.models import Produto
    from db.models import Pedido
except:
    from lista_supermercado_mysql.db.models import Produto
    from lista_supermercado_mysql.db.models import Pedido

class ProdutoRepository:
    @staticmethod
    def listar_produtos(db: Session) -> list[Produto]:
        return db.query(Produto).all()

    @staticmethod
    def adicionar_produto(db: Session, produto: Produto) -> Produto:
        db.add(produto)
        db.commit()
        return produto
    
    def atualizar_produto(db: Session, produto: Produto) -> Produto:
        db.merge(produto)
        db.commit()
        return produto

    @staticmethod
    def encontrar_produto_por_id(db: Session, id: int) -> Produto:
        return db.query(Produto).filter(Produto.id == id).first()

    @staticmethod
    def existe_produto_por_id(db: Session, id: int) -> bool:
        return db.query(Produto).filter(Produto.id == id).first() is not None

    @staticmethod
    def apagar_produto_por_id(db: Session, id: int) -> None:
        produto = db.query(Produto).filter(Produto.id == id).first()
        if produto is not None:
            db.delete(produto)
            db.commit()

    @staticmethod
    def apagar_todos_produtos(db: Session) -> None:
        db.query(Produto).delete()
        db.commit()
        
    @staticmethod
    def listar_produtos_por_tipo(db : Session, type : str)->list[Produto]:
    
        return db.query(Produto).filter(Produto.tipo == type).all()
    
    @staticmethod
    def check_item(db: Session, item : str) ->list[Produto]:
        return db.query(Produto).filter(Produto.item == item).all()
        
           
class PedidoRepository:
     
    @staticmethod
    def listar_pedidos(db: Session) -> list[Pedido]:
        
        return db.query(Pedido).all()
    
    @staticmethod
    def adicionar_pedido(db: Session,  pedido: Pedido) -> Pedido:
        
        pedidos = pedido.produtos.split(",")
        pedido_fora_do_banco = []
        preco =  0
        for ped in pedidos:
            produto_banco =  db.query(Produto).filter(Produto.item == ped).first()
            if produto_banco is not None:
                
                preco = preco +  produto_banco.preco
            else:
                preco = preco + 0
                pedido_fora_do_banco.append(ped)
                
        pedidos = [ item for item in pedidos if item not in pedido_fora_do_banco]
        pedido.produtos = ','.join(pedidos)
         
        pedido.preco = preco 
        db.add(pedido)
        db.commit()
        
        return pedido
    
    @staticmethod
    def existe_pedido_por_id(db: Session, id: int) -> bool:
        return db.query(Pedido).filter(Pedido.id == id).first() is not None
    
    @staticmethod
    def atualizar_pedido(db: Session, pedido: Pedido) -> Pedido:
        pedidos = pedido.produtos.split(",")
        pedido_fora_do_banco = []
        preco =  0
        for ped in pedidos:
            produto_banco =  db.query(Produto).filter(Produto.item == ped).first()
            if produto_banco is not None:
                
                preco = preco +  produto_banco.preco
            else:
                preco = preco + 0
                pedido_fora_do_banco.append(ped)
                
        pedidos = [ item for item in pedidos if item not in pedido_fora_do_banco]
        pedido.produtos = ','.join(pedidos)
         
        pedido.preco = preco   
        db.merge(pedido)
        db.commit()
        return pedido
       
     
        
    
    
        
        