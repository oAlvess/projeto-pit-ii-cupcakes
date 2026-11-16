"""Conexão com o banco de dados SQLite."""
import sqlite3
from flask import current_app, g


def get_db():
    """Abre (uma vez por requisição) a conexão com o banco."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
        g.db.execute("PRAGMA foreign_keys = ON")  # ativa as chaves estrangeiras
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Cria as tabelas e os dados iniciais a partir do schema.sql."""
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf-8"))
        db.commit()
