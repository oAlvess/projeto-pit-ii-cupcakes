"""Testes automatizados das rotas principais."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app

def criar_app_teste():
    pasta = tempfile.mkdtemp()
    return create_app({"DATABASE": os.path.join(pasta, "teste.db"), "TESTING": True, "SECRET_KEY": "teste"})

def test_cardapio_abre_e_lista_produtos():
    resposta = criar_app_teste().test_client().get("/")
    assert resposta.status_code == 200
    assert "Chocolate" in resposta.get_data(as_text=True)

def test_preco_formatado_em_reais():
    html = criar_app_teste().test_client().get("/").get_data(as_text=True)
    assert "R$ 8,50" in html

def test_filtro_por_categoria():
    html = criar_app_teste().test_client().get("/?categoria=3").get_data(as_text=True)
    assert "Cenoura vegano" in html and "Chocolate" not in html

def test_busca_por_nome():
    html = criar_app_teste().test_client().get("/?busca=Chocolate").get_data(as_text=True)
    assert "Chocolate" in html and "Baunilha" not in html

def test_adicionar_ao_carrinho_e_visualizar():
    client = criar_app_teste().test_client()
    resposta = client.post("/carrinho/adicionar/1", follow_redirects=True)
    assert resposta.status_code == 200
    html = client.get("/carrinho").get_data(as_text=True)
    assert "Chocolate" in html and "R$ 8,50" in html

def test_remover_item_do_carrinho():
    client = criar_app_teste().test_client()
    client.post("/carrinho/adicionar/1")
    client.post("/carrinho/remover/1")
    html = client.get("/carrinho").get_data(as_text=True)
    assert "Seu carrinho está vazio" in html

def test_finalizar_pedido_com_dados_validos():
    client = criar_app_teste().test_client()
    client.post("/carrinho/adicionar/1")
    resposta = client.post("/finalizar", data={"nome":"Pessoa Teste", "email":"teste@example.com", "endereco":"Rua de Teste, 123"})
    assert resposta.status_code == 200
    assert "Pedido registrado" in resposta.get_data(as_text=True)

def test_finalizar_sem_carrinho_redireciona():
    resposta = criar_app_teste().test_client().get("/finalizar")
    assert resposta.status_code == 302
