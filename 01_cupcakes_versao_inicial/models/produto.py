"""Model: acesso aos dados de produtos e categorias."""
from database import get_db


def listar_categorias():
    return get_db().execute(
        "SELECT id_categoria, nome FROM categoria ORDER BY nome"
    ).fetchall()


def listar_ativos(id_categoria=None):
    """Retorna os produtos ativos, com filtro opcional por categoria."""
    sql = (
        "SELECT p.id_produto, p.nome, p.descricao, p.preco, p.estoque, "
        "c.nome AS categoria "
        "FROM produto p JOIN categoria c ON c.id_categoria = p.id_categoria "
        "WHERE p.ativo = 1"
    )
    params = []
    if id_categoria:
        sql += " AND p.id_categoria = ?"
        params.append(id_categoria)
    sql += " ORDER BY p.nome"
    return get_db().execute(sql, params).fetchall()


def buscar_por_id(id_produto):
    return get_db().execute(
        "SELECT * FROM produto WHERE id_produto = ? AND ativo = 1", (id_produto,)
    ).fetchone()
