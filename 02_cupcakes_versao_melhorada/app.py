"""Ponto de entrada do aplicativo de vendas de cupcakes."""
import os
from flask import Flask
import database
from controllers import cardapio


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        DATABASE=os.path.join(app.root_path, "cupcakes.db"),
        SECRET_KEY=os.environ.get("SECRET_KEY", "chave-local-de-desenvolvimento"),
    )
    if config:
        app.config.update(config)

    if not os.path.exists(app.config["DATABASE"]):
        database.init_db(app)

    app.teardown_appcontext(database.close_db)
    app.register_blueprint(cardapio.bp)

    @app.template_filter("brl")
    def formatar_reais(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
