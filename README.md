# Pipeline de Controle de Gastos — Olist

Projeto final de engenharia e análise de dados sobre comportamento de gastos em compras online. O objetivo é responder perguntas diferentes de um pipeline genérico de vendas: **como o gasto evolui no tempo, quais estados concentram o consumo, como os clientes pagam e quão concentrado é o gasto por cliente?**

## Fonte e licença

Fonte: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), baixado pela API pública do Kaggle. O dataset é distribuído sob licença **CC BY-NC-SA 4.0** na página da fonte. Este repositório é público para fins educacionais e mantém a atribuição à fonte. O download é reproduzível pelo script `scripts/download_data.py`.

## O que é uma linha de cada tabela

- `olist_orders_dataset.csv`: uma linha por pedido.
- `olist_order_payments_dataset.csv`: uma linha por parcela/método de pagamento de um pedido.
- `olist_customers_dataset.csv`: uma linha por cliente e seu endereço de entrega.
- `olist_order_items_dataset.csv`: uma linha por item de um pedido.

As tabelas são ligadas por `order_id` e `customer_id`. O pipeline usa JOIN entre pedidos, pagamentos e clientes.

## Camadas

1. **Raw** (`data/raw/`): arquivos originais baixados, sem alteração.
2. **Refined** (`data/refined/`): dados tipados, padronizados e ligados por SQL em DuckDB; datas são convertidas e valores são agregados em nível de pedido/cliente.
3. **Marts** (`data/marts/`): tabelas finais de indicadores, cada uma com seu SQL de origem em `sql/marts/`.

## Indicadores produzidos

- `monthly_spend_by_state.csv`: pedidos, clientes, valor pago, ticket médio e clientes ativos por mês/estado.
- `payment_method_mix.csv`: valor pago, quantidade de pedidos, participação no valor e parcelas médias por método.
- `customer_spend_profile.csv`: total gasto, pedidos, ticket médio e primeiro/último pedido por cliente.

## Como rodar do zero

Requisitos: Python 3.10+.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python scripts/download_data.py
python -m src.run_pipeline
pytest -q
```

O pipeline lê os CSVs de `data/raw`, executa os SQLs com DuckDB e grava CSVs em `data/refined` e `data/marts`. Os arquivos de dados gerados não são versionados; o download é reproduzível.

Opcionalmente, para abrir o dashboard:

```bash
streamlit run dashboard/app.py
```

O dashboard lê somente `data/marts`; não faz cálculos de negócio na tela.

## Histórico de commits

O trabalho foi construído em etapas: estrutura e documentação; download e camada raw; transformações refined; indicadores marts; testes; dashboard e revisão final. Cada etapa possui um commit próprio, com mensagem explicando o que mudou.

## Onde a IA errou ou assumiu algo

A IA inicialmente assumiu que o projeto de Controle de Gastos deveria continuar apenas como uma aplicação front-end. Isso não atendia ao desafio, que exige fonte de dados, camadas, SQL e testes. A correção foi separar este pipeline analítico em um repositório próprio e definir perguntas novas: evolução temporal do gasto, concentração por estado/cliente e mix de pagamento.

Durante a conferência, também foi validado que `order_payments` pode ter várias linhas para o mesmo pedido; por isso, o indicador de pedidos usa `COUNT(DISTINCT order_id)` e o valor usa a soma das parcelas, evitando contar o pedido várias vezes. As contagens de linhas e chaves são verificadas em `tests/test_transform.py` com dados inventados, sem abrir o banco do projeto.
