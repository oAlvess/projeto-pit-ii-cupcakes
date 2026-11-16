-- Projeto físico do banco (SQLite) - aplicativo de vendas de cupcakes

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nome       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    telefone   TEXT,
    perfil     TEXT NOT NULL DEFAULT 'cliente' CHECK (perfil IN ('cliente', 'admin')),
    criado_em  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS produto (
    id_produto   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    descricao    TEXT,
    preco        REAL NOT NULL CHECK (preco > 0),
    estoque      INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    ativo        INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente       INTEGER NOT NULL,
    data_pedido      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status           TEXT NOT NULL DEFAULT 'aguardando_pagamento'
                     CHECK (status IN ('aguardando_pagamento', 'pago', 'em_preparo', 'entregue', 'cancelado')),
    valor_total      REAL NOT NULL DEFAULT 0,
    endereco_entrega TEXT NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
);

CREATE TABLE IF NOT EXISTS item_pedido (
    id_item        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido      INTEGER NOT NULL,
    id_produto     INTEGER NOT NULL,
    quantidade     INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL NOT NULL,
    UNIQUE (id_pedido, id_produto),
    FOREIGN KEY (id_pedido)  REFERENCES pedido (id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
);

CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido      INTEGER NOT NULL UNIQUE,
    forma          TEXT NOT NULL CHECK (forma IN ('pix', 'cartao', 'dinheiro')),
    valor          REAL NOT NULL,
    status         TEXT NOT NULL DEFAULT 'pendente' CHECK (status IN ('pendente', 'aprovado', 'recusado')),
    data_pagamento TEXT,
    FOREIGN KEY (id_pedido) REFERENCES pedido (id_pedido)
);

-- Dados iniciais para testes
INSERT OR IGNORE INTO categoria (id_categoria, nome) VALUES
    (1, 'Tradicionais'), (2, 'Gourmet'), (3, 'Veganos');

INSERT INTO produto (nome, descricao, preco, estoque, id_categoria)
SELECT * FROM (
    SELECT 'Chocolate', 'Massa de chocolate com cobertura de brigadeiro', 8.50, 30, 1
    UNION ALL SELECT 'Baunilha', 'Massa de baunilha com buttercream', 7.50, 30, 1
    UNION ALL SELECT 'Red Velvet', 'Massa red velvet com cream cheese', 11.00, 20, 2
    UNION ALL SELECT 'Cenoura vegano', 'Cenoura com cobertura de chocolate sem leite', 9.50, 15, 3
) WHERE NOT EXISTS (SELECT 1 FROM produto);
