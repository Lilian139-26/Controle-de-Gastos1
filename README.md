# Pipeline de Controle de Gastos — Controle-de-Gastos

Projeto final de engenharia e análise de dados construído sobre o domínio do aplicativo **Controle de Gastos**. O pipeline usa uma fonte pública real para gerar análises reproduzíveis e também inclui um contrato para ler um export sanitizado do app, com as mesmas entidades: cartões, contas fixas, contas adicionais e ganhos.

As perguntas analíticas são: **como o gasto evolui no tempo, quais estados concentram o consumo, como os clientes pagam e, no formato do app, qual é o saldo mensal depois de despesas e ganhos?**

## Fonte e licença

Fonte: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), baixado pela API pública do Kaggle. O dataset é distribuído sob licença **CC BY-NC-SA 4.0** na página da fonte. Este repositório é público para fins educacionais e mantém a atribuição à fonte. O download é reproduzível pelo script `scripts/download_data.py`.

## O que é uma linha de cada tabela

- `olist_orders_dataset.csv`: uma linha por pedido.
- `olist_order_payments_dataset.csv`: uma linha por parcela/método de pagamento de um pedido.
- `olist_customers_dataset.csv`: uma linha por cliente e seu endereço de entrega.
- `olist_order_items_dataset.csv`: uma linha por item de um pedido.

As tabelas são ligadas por `order_id` e `customer_id`. O pipeline usa JOIN entre pedidos, pagamentos e clientes.

## Relação com o aplicativo Controle de Gastos

O site publicado em [lilian139-26.github.io/controle-gastos](https://lilian139-26.github.io/controle-gastos/) é a interface do projeto. Este repositório é a camada analítica separada: não contém os dados pessoais salvos no app e não acessa a conta Supabase de ninguém.

O módulo `src/app_contract.py` traduz um export sanitizado do formato do app para linhas analíticas. Ele reconhece `cartoes`, `contasFixas`, `contasAdicionais` e `ganhos`, e produz os indicadores mensais `expenses`, `income` e `balance`. Os testes desse contrato usam apenas dados inventados, sem banco e sem dados da usuária.

## Camadas

1. **Raw** (`data/raw/`): arquivos originais baixados, sem alteração.
2. **Refined** (`data/refined/`): dados tipados, padronizados e ligados por SQL em DuckDB; datas são convertidas e valores são agregados em nível de pedido/cliente.
3. **Marts** (`data/marts/`): tabelas finais de indicadores, cada uma com seu SQL de origem em `sql/marts/`.

## Indicadores produzidos

- `monthly_spend_by_state.csv`: pedidos, clientes, valor pago, ticket médio e clientes ativos por mês/estado.
- `payment_method_mix.csv`: valor pago, quantidade de pedidos, participação no valor e parcelas médias por método.
- `customer_spend_profile.csv`: total gasto, pedidos, ticket médio e primeiro/último pedido por cliente.
- Contrato do app: transações mensais por tipo e saldo (`src/app_contract.py`), pronto para receber um export sanitizado sem credenciais ou valores pessoais.

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

Para validar o formato do aplicativo, os testes do contrato já rodam com `pytest`. Um export real do app só deve ser usado se estiver sanitizado e autorizado; ele não deve ser commitado no repositório público.

Opcionalmente, para abrir o dashboard:

```bash
streamlit run dashboard/app.py
```

O dashboard lê somente `data/marts`; não faz cálculos de negócio na tela.

## Histórico de commits

O trabalho foi construído em etapas: estrutura e documentação; download e camada raw; transformações refined; indicadores marts; testes; dashboard e revisão final. Cada etapa possui um commit próprio, com mensagem explicando o que mudou.

## Onde a IA errou ou assumiu algo

A IA inicialmente assumiu que o projeto de Controle de Gastos deveria continuar apenas como uma aplicação front-end. Isso não atendia ao desafio, que exige fonte de dados, camadas, SQL e testes. A correção foi manter o app como interface e construir este pipeline em cima do seu domínio, com uma fonte pública real e um adaptador para o formato de cartões, contas e ganhos.

Durante a conferência, também foi validado que `order_payments` pode ter várias linhas para o mesmo pedido; por isso, o indicador de pedidos usa `COUNT(DISTINCT order_id)` e o valor usa a soma das parcelas, evitando contar o pedido várias vezes. As contagens de linhas e chaves são verificadas em `tests/test_transform.py` com dados inventados, sem abrir o banco do projeto.

Outra correção foi separar o armazenamento local por usuário no app: dados da conta pessoal não devem ser copiados para a conta genérica de demonstração. Essa alteração foi publicada no repositório do site, enquanto este pipeline permanece sem dados pessoais.
