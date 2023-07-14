"""Lista de Supermercado"""

# Bibliotecas
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


# quando for executar o servidor
try:
    from schemas.produto import ProdutoBase, ProdutoRequest, ProdutoResponse
    from schemas.pedido import PedidoBase, PedidoRequest, PedidoResponse
    from db.models import Produto, Pedido
    from db.repositories import ProdutoRepository, PedidoRepository
    from db.database import engine, Base, get_db
    
# quando for executar os testes
except ImportError:
    from lista_supermercado_mysql.schemas.produto import ProdutoBase, ProdutoRequest, ProdutoResponse
    from lista_supermercado_mysql.schemas.pedido import PedidoBase, PedidoRequest, PedidoResponse
    from lista_supermercado_mysql.db.models import Produto, Pedido
    from lista_supermercado_mysql.db.repositories import ProdutoRepository
    from lista_supermercado_mysql.db.database import engine, Base, get_db


# Configuração de acesso ao Banco de Dados
Base.metadata.create_all(bind=engine)

# Cria uma instância da classe FastAPI para habilitar a interação com nossa API
app = FastAPI()

origins = ["http://0.0.0.0:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tratamento de exceções
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, err):
    return JSONResponse(
        status_code = 400,
        content = {"error": str(err)},
    )

# @app.get('/produtos') informa ao FastAPI que esta função gerenciará as
# requisições quando for requisitada a rota GET /produtos
@app.get('/produtos')
async def listar_produtos(db: Session = Depends(get_db)):
    """Método que será chamado quando for requisitada a rota GET /produtos"""

    # pesquisa na base de dados
    produtos = ProdutoRepository.listar_produtos(db)
    
    if len(produtos) > 0 :
        return [ProdutoResponse.from_orm(produto) for produto in produtos]
    else:
        return JSONResponse(
            status_code = 200,
            content = {"message": "A lista de produtos está vazia!"},
        ) 

  
# @app.post('/produtos') informa ao FastAPI que esta função gerenciará as
# requisições quando for requisitada a rota POST /produtos
@app.post('/produtos')
async def adicionar_produto(request: ProdutoRequest, db: Session = Depends(get_db)):
    """Método que será chamado quando for requisitada a rota POST /produtos"""
  
    if len(ProdutoRepository.check_item(db, Produto(**request.dict()).item )) > 0 :
       
        return JSONResponse(
            status_code = 404,
            content = {"message": f"Produto {Produto(**request.dict()).item} já exite!"},
       )
    else:
        produto = ProdutoRepository.adicionar_produto(db, Produto(**request.dict()))
        
        return ProdutoResponse.from_orm(produto)

# @app.put('/produtos/{id}') informa ao FastAPI que esta função gerenciará as
# requisições quando for requisitada a rota PUT /produtos/{id}
@app.put('/produtos/{id}')
async def atualizar_produto(id: int, request: ProdutoRequest, db: Session = Depends(get_db)):
    """Método que será chamado quando for requisitada a rota PUT /produtos/{id}"""

    if not ProdutoRepository.existe_produto_por_id(db, id):
        return JSONResponse(
            status_code = 404,
            content = {"message": f"Produto {id} não foi encontrado na lista!"},
        )
    else:
        produto = ProdutoRepository.atualizar_produto(db, Produto(id=id, **request.dict()))
        return ProdutoResponse.from_orm(produto)

# @app.delete('/produtos/{id}') informa ao FastAPI que esta função gerenciará as
# requisições quando for requisitada a rota DELETE /produtos/{id}
@app.delete('/produtos/{id}')
async def apagar_produto(id: int, db: Session = Depends(get_db)):
    """Método que será chamado quando for requisitada a rota DELETE /produtos/{id}"""
    
    if not ProdutoRepository.existe_produto_por_id(db, id):
        return JSONResponse(
            status_code = 404,
            content = {"message": "Produto " + str(id) + " não foi encontrado na lista!"},
        )
    else:
        produto = ProdutoRepository.apagar_produto_por_id(db, id)
        return JSONResponse(
            status_code = 200,
            content = {"message": "Produto id=" + str(id) + " apagado com sucesso!"},
        )
    


@app.get('/pedidos')
async def listar_pedido(db: Session = Depends(get_db)):
    #M que será chamado quando for requisitada a rota GET /produtos

    # pesquisa na base de dados
    pedidos =  PedidoRepository.listar_pedidos(db)
    #ids_list = db.query(Produto).filter(Produto.id == id).first()
    if len(pedidos) > 0 :
        
        return [PedidoResponse.from_orm(pedido) for pedido in pedidos]
    
    
    else:
        return JSONResponse(
            status_code = 200,
            content = {"message": "A lista de pedidos está vazia!"},
        )


@app.post('/pedidos')
async def adicionar_pedidos(request: PedidoRequest, db: Session = Depends(get_db)):
    # Para adicionar o pedidos digite o nome do produto, separado por virulas 
    # ex : {
    #           "produtos": "coca-cola,hamburguer"
    #      }
    #
   
    pedido = PedidoRepository.adicionar_pedido(db, Pedido(**request.dict()))
    # {"pedido": PedidoResponse.from_orm(pedido), "produtos_disponiveis": produtos_disponiveis}
                    #return [ProdutoResponse.from_orm(produto) for produto in produtos]

    return PedidoResponse.from_orm(pedido)


@app.put('/pedidos/{id}')
async def Remover_item_do_pedido(id: int, request: PedidoRequest, db: Session = Depends(get_db)):
    """Método que será chamado quando for requisitada a rota PUT /produtos/{id}"""

    if not PedidoRepository.existe_pedido_por_id(db, id):
        return JSONResponse(
            status_code = 404,
            content = {"message": f"Pedido {id} não foi encontrado!"},
        )
    else:
        pedido = PedidoRepository.atualizar_pedido(db, Pedido(id=id, **request.dict()))
        return PedidoResponse.from_orm(pedido)


@app.get('/produtos/')
async def lista_produtos_by_type(type : str, db: Session = Depends(get_db)):
    if check_type(type):
        produtos = ProdutoRepository.listar_produtos_por_tipo(db,type)
        if len(produtos) > 0 :
            return [ProdutoResponse.from_orm(produto) for produto in produtos]
        else:
            return JSONResponse(
                status_code = 200,
                content = {"message": "A lista de pedidos está vazia!"},
            )
    else:
        return JSONResponse(
                status_code = 200,
                content = {"message": "Tipo não encontrado!"},
            )

def check_type(type):
    return type in ['comida', 'bebida']



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, log_level="info", reload=True)
    print("running")
