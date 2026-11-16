"""Rotas do cardápio e do carrinho."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import produto

bp = Blueprint("cardapio", __name__)


@bp.route("/")
def listar():
    categoria = request.args.get("categoria", type=int)
    busca = request.args.get("busca", "").strip()[:80]
    return render_template(
        "cardapio.html",
        produtos=produto.listar_ativos(categoria, busca),
        categorias=produto.listar_categorias(),
        categoria_atual=categoria,
        busca=busca,
        carrinho_total=sum(int(q) for q in session.get("carrinho", {}).values()),
    )


@bp.post("/carrinho/adicionar/<int:id_produto>")
def adicionar_carrinho(id_produto):
    item = produto.buscar_por_id(id_produto)
    if item is None:
        flash("Este cupcake não está disponível.", "erro")
        return redirect(url_for("cardapio.listar"))
    carrinho = session.get("carrinho", {})
    chave = str(id_produto)
    atual = int(carrinho.get(chave, 0))
    if item["estoque"] <= atual:
        flash("Quantidade indisponível em estoque.", "erro")
    else:
        carrinho[chave] = atual + 1
        session["carrinho"] = carrinho
        flash(f'{item["nome"]} adicionado ao carrinho.', "sucesso")
    return redirect(request.referrer or url_for("cardapio.listar"))


@bp.get("/carrinho")
def ver_carrinho():
    carrinho = session.get("carrinho", {})
    itens = []
    total = 0.0
    for chave, quantidade in carrinho.items():
        item = produto.buscar_por_id(int(chave))
        if item:
            subtotal = float(item["preco"]) * int(quantidade)
            itens.append({"produto": item, "quantidade": int(quantidade), "subtotal": subtotal})
            total += subtotal
    return render_template("carrinho.html", itens=itens, total=total)


@bp.post("/carrinho/remover/<int:id_produto>")
def remover_carrinho(id_produto):
    carrinho = session.get("carrinho", {})
    carrinho.pop(str(id_produto), None)
    session["carrinho"] = carrinho
    flash("Item removido do carrinho.", "sucesso")
    return redirect(url_for("cardapio.ver_carrinho"))


@bp.post("/carrinho/limpar")
def limpar_carrinho():
    session.pop("carrinho", None)
    flash("Carrinho limpo.", "sucesso")
    return redirect(url_for("cardapio.ver_carrinho"))


@bp.route("/finalizar", methods=["GET", "POST"])
def finalizar_pedido():
    carrinho = session.get("carrinho", {})
    if not carrinho:
        flash("Adicione pelo menos um produto antes de finalizar.", "erro")
        return redirect(url_for("cardapio.listar"))
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()[:100]
        email = request.form.get("email", "").strip().lower()[:150]
        endereco = request.form.get("endereco", "").strip()[:250]
        if not nome or "@" not in email or not endereco:
            flash("Preencha nome, e-mail válido e endereço.", "erro")
            return render_template("finalizar.html")
        db = produto.get_db()
        try:
            db.execute("BEGIN")
            cliente = db.execute("SELECT id_cliente FROM cliente WHERE email = ?", (email,)).fetchone()
            if cliente:
                id_cliente = cliente["id_cliente"]
                db.execute("UPDATE cliente SET nome = ? WHERE id_cliente = ?", (nome, id_cliente))
            else:
                cursor = db.execute("INSERT INTO cliente (nome, email, senha_hash) VALUES (?, ?, ?)", (nome, email, "pedido-sem-login"))
                id_cliente = cursor.lastrowid
            linhas = []
            total = 0.0
            for chave, quantidade in carrinho.items():
                item = db.execute("SELECT id_produto, nome, preco, estoque, ativo FROM produto WHERE id_produto = ?", (int(chave),)).fetchone()
                quantidade = int(quantidade)
                if item is None or not item["ativo"] or quantidade < 1 or item["estoque"] < quantidade:
                    raise ValueError("Estoque insuficiente para um dos itens. Revise o carrinho.")
                linhas.append((item, quantidade))
                total += float(item["preco"]) * quantidade
            cursor = db.execute("INSERT INTO pedido (id_cliente, valor_total, endereco_entrega) VALUES (?, ?, ?)", (id_cliente, total, endereco))
            id_pedido = cursor.lastrowid
            for item, quantidade in linhas:
                db.execute("INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES (?, ?, ?, ?)", (id_pedido, item["id_produto"], quantidade, item["preco"]))
                db.execute("UPDATE produto SET estoque = estoque - ? WHERE id_produto = ?", (quantidade, item["id_produto"]))
            db.commit()
        except (ValueError, Exception) as erro:
            db.rollback()
            flash(str(erro) if isinstance(erro, ValueError) else "Não foi possível registrar o pedido. Tente novamente.", "erro")
            return redirect(url_for("cardapio.ver_carrinho"))
        session.pop("carrinho", None)
        return render_template("pedido_confirmado.html", id_pedido=id_pedido, total=total)
    return render_template("finalizar.html")
