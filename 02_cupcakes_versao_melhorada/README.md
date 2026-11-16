# Cupcakes — versão melhorada (PIT II)

Aplicação demonstrativa de cardápio e pedidos de cupcakes, evoluída a partir do projeto-base recebido.

## Melhorias incluídas
- Busca de produtos por nome ou descrição, combinável com filtro de categoria.
- Carrinho por sessão: adicionar, visualizar, remover e limpar itens.
- Finalização de pedido com validação de nome, e-mail e endereço.
- Registro de cliente, pedido e itens no SQLite em transação.
- Verificação de estoque antes de confirmar e baixa do estoque após o registro.
- Mensagens de retorno, telas de carrinho e confirmação, metadados e layout responsivo.
- Testes automatizados para cardápio, filtros, busca, carrinho e finalização.

## Tecnologias
Python, Flask, SQLite, HTML, CSS, Jinja2 e Pytest. Arquitetura organizada em rotas (controllers), consultas (models), templates e camada de banco.

## Executar localmente
1. Instale Python 3.10 ou superior.
2. (Recomendado) Crie um ambiente virtual: `python -m venv .venv`.
3. Ative-o e instale: `pip install -r requirements.txt`.
4. Execute: `python app.py`.
5. Abra `http://127.0.0.1:5000`.

O banco `cupcakes.db` é criado automaticamente na primeira execução.

## Executar testes
`pytest -q`

## Observações acadêmicas
Este é um protótipo didático. O cadastro simplificado de cliente não implementa autenticação; o valor `senha_hash` é preenchido com um marcador para satisfazer o esquema original. Não use dados reais. Pagamento, integração com gateway, autenticação e publicação em hospedagem ainda não fazem parte desta versão.
