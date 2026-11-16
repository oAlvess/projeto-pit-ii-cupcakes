"""Controller: tela do cardápio."""
from flask import Blueprint, render_template, request
from models import produto

bp = Blueprint("cardapio", __name__)


@bp.route("/")
def listar():
    # O filtro de categoria vem da URL, ex.: /?categoria=2
    id_categoria = request.args.get("categoria", type=int)
    return render_template(
        "cardapio.html",
        produtos=produto.listar_ativos(id_categoria),
        categorias=produto.listar_categorias(),
        categoria_atual=id_categoria,
    )
