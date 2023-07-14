from fastapi.testclient import TestClient
from lista_supermercado_mysql.main import app

client = TestClient(app)

    
def test_listar_produtos_lista_vazia():
    response = client.delete('/produtos/')
    response = client.get('/produtos')
    assert response.status_code == 200
    assert response.json() == {"message": "A lista de produtos está vazia!"}

def test_listar_produtos_lista_com_um_item():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste1", "quantidade": 5, "preco": 5, "tipo":"comida"})
    assert response.status_code == 200
    
    response = client.get('/produtos')
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    produto = response.json()[0]
    assert produto['item'] == "teste1"
    assert produto['quantidade'] == 5
    assert produto['preco'] == 5
    assert produto['tipo'] == "comida"

def test_obter_produto_especifico():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste2", "quantidade": 10, "preco": 2.5, "tipo":"bebida"})

    response = client.get('/produtos/'+ str(response.json()['id']))
    assert response.json()['item'] == "teste2"
    assert response.json()['quantidade'] == 10

def test_atualizar_produto():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste3", "quantidade": 3, "preco": 2.5, "tipo":"bebida"})
    
    produto_id = response.json()['id']
    
    response = client.put(f'/produtos/{produto_id}', json={"quantidade": 5, "preco": 3.0})
    
    assert response.status_code == 200
    assert response.json()['id'] == produto_id
    assert response.json()['item'] == "teste3"
    assert response.json()['quantidade'] == 5
    assert response.json()['preco'] == 3.0
    assert response.json()['tipo'] == "bebida"

def test_remover_produto():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste4", "quantidade": 2, "preco": 4.5, "tipo":"bebida"})
    
    produto_id = response.json()['id']
    
    response = client.delete(f'/produtos/{produto_id}')
    
    assert response.status_code == 200
    assert response.json() == {"message": "Produto removido com sucesso"}

    
def test_lista_produtos_por_tipo():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste17", "quantidade": 8, "preco": 2.0, "tipo":"comida"})
    response = client.post('/produtos', json={"item": "teste18", "quantidade": 3, "preco": 1.5, "tipo":"comida"})
    response = client.post('/produtos', json={"item": "teste19", "quantidade": 5, "preco": 4.0, "tipo":"comida"})
    
    response = client.get('/produtos?tipo=comida')
    assert response.status_code == 200
    assert len(response.json()) == 2
    for produto in response.json():
        assert produto['tipo'] == 'comida'

def test_lista_produtos_por_tipo_inexistente():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste20", "quantidade": 5, "preco": 2.0, "tipo":"bebida"})
    response = client.post('/produtos', json={"item": "teste21", "quantidade": 3, "preco": 1.5, "tipo":"comida"})
    
    response = client.get('/produtos?tipo=limpeza')
    assert response.status_code == 200
    assert len(response.json()) == 0
    assert response.json()['message'] == 'A lista de produtos está vazia!'


def test_listar_produtos_por_quantidade_minima():
    response = client.delete('/produtos/')
    
    response = client.post('/produtos', json={"item": "teste8", "quantidade": 10, "preco": 3.0, "tipo":"bebida"})
    response = client.post('/produtos', json={"item": "teste9", "quantidade": 5, "preco": 2.5, "tipo":"comida"})
    response = client.post('/produtos', json={"item": "teste10", "quantidade": 3, "preco": 1.0, "tipo":"comida"})
    
    response = client.get('/produtos?quantidade_minima=5')
    assert response.status_code == 200
    assert len(response.json()) == 2
    for produto in response.json():
        assert produto['quantidade'] >= 5