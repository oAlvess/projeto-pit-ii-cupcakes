"""Testes do cardápio (execute com: pytest)."""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app


def criar_cliente_de_teste():
    caminho = os.path.join(tempfile.mkdtemp(), "teste.db")
    app = create_app({"DATABASE": caminho, "TESTING": True})
    return app.test_client()


def test_cardapio_abre_e_lista_produtos():
    resposta = criar_cliente_de_teste().get("/")
    assert resposta.status_code == 200
    assert "Chocolate" in resposta.get_data(as_text=True)


def test_preco_formatado_em_reais():
    html = criar_cliente_de_teste().get("/").get_data(as_text=True)
    assert "R$ 8,50" in html


def test_filtro_por_categoria():
    html = criar_cliente_de_teste().get("/?categoria=3").get_data(as_text=True)
    assert "Cenoura vegano" in html
    assert "Chocolate" not in html


def test_categoria_inexistente_mostra_aviso():
    html = criar_cliente_de_teste().get("/?categoria=999").get_data(as_text=True)
    assert "Nenhum cupcake encontrado" in html
