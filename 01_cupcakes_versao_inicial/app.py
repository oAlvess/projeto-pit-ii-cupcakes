"""Ponto de entrada do aplicativo de vendas de cupcakes."""
import os
from flask import Flask
import database
from controllers import cardapio


def create_app(config=None):
    app = Flask(__name__)
    app.config["DATABASE"] = os.path.join(app.root_path, "cupcakes.db")
    app.config["SECRET_KEY"] = "troque-esta-chave-depois"
    if config:
        app.config.update(config)

    # Cria o banco na primeira execução
    if not os.path.exists(app.config["DATABASE"]):
        database.init_db(app)

    app.teardown_appcontext(database.close_db)
    app.register_blueprint(cardapio.bp)

    @app.template_filter("brl")
    def formatar_reais(valor):
        """8.5 -> 'R$ 8,50'"""
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
