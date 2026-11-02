# Controle de Gastos com dados da Olist

Projeto final de engenharia e análise de dados desenvolvido com Python, SQL, DuckDB, testes e Git. O tema do projeto é **Controle de Gastos**: a análise trata o valor pago nos pedidos da Olist como gasto de compra e organiza indicadores para entender evolução, concentração e formas de pagamento.

O aplicativo visual Controle de Gastos foi a inspiração do tema e da linguagem do projeto. Este pipeline é um projeto analítico independente: ele **não acessa o Supabase, não usa os dados pessoais do aplicativo e não contém login ou senha**.

## Perguntas do projeto

1. Como o gasto total evolui mês a mês?
2. Quais estados concentram o maior valor pago?
3. Qual é o ticket médio por mês e estado?
4. Quais formas de pagamento concentram os gastos?
5. Quais clientes possuem maior gasto acumulado e qual é a frequência de pedidos?

Essas perguntas usam a Olist de uma maneira orientada a controle de gastos, em vez de copiar um painel genérico de vendas.

## Fonte e licença

Fonte: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), baixado pela API pública do Kaggle. O dataset é distribuído sob licença **CC BY-NC-SA 4.0** na página da fonte. Este repositório é público para fins educacionais e mantém a atribuição à fonte. O download é reproduzível pelo script `scripts/download_data.py`.

## O que é uma linha de cada tabela

- `olist_orders_dataset.csv`: uma linha por pedido.
- `olist_order_payments_dataset.csv`: uma linha por parcela ou método de pagamento de um pedido.
- `olist_customers_dataset.csv`: uma linha por cliente e endereço de entrega.
- `olist_order_items_dataset.csv`: uma linha por item de um pedido.

As tabelas são ligadas por `order_id` e `customer_id`, permitindo os JOINs usados nas camadas refinadas e nos indicadores.

## Camadas do pipeline

1. **Raw** (`data/raw/`): arquivos originais baixados da fonte, sem alteração.
2. **Refined** (`data/refined/`): pedidos e pagamentos tipados, datas convertidas, pagamentos agregados por pedido e pedidos ligados aos clientes.
3. **Marts** (`data/marts/`): tabelas finais de indicadores de controle de gastos, cada uma produzida por um SQL correspondente em `sql/marts/`.

## Indicadores produzidos

- `monthly_spend_by_state.csv`: mês, estado, quantidade de pedidos, clientes ativos, gasto total e ticket médio.
- `payment_method_mix.csv`: forma de pagamento, pedidos, gasto total, participação no valor e média de parcelas.
- `customer_spend_profile.csv`: cliente, estado, quantidade de pedidos, gasto acumulado, ticket médio e período de atividade.

Cada indicador possui um arquivo `.sql` de origem. O valor de um pedido é calculado pela soma das parcelas em `order_payments`; a quantidade de pedidos usa `COUNT(DISTINCT order_id)` para não contar duas vezes um pedido parcelado.

## Como rodar do zero

Requisitos: Python 3.10+.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python scripts/download_data.py
python -m src.run_pipeline
pytest -q
```

O pipeline baixa a fonte para `data/raw`, executa as transformações e SQLs com DuckDB e grava os resultados em `data/refined` e `data/marts`. Os CSVs de dados não são versionados no Git; qualquer pessoa consegue recriá-los seguindo os comandos acima.

Opcionalmente, para abrir o dashboard:

```bash
streamlit run dashboard/app.py
```

O dashboard opcional lê somente os arquivos da camada `data/marts`; não faz cálculos de negócio na tela.

## Histórico de commits

O projeto foi construído em etapas, com commits separados: documentação e estrutura; download da fonte e camada raw; transformações da camada refined; indicadores marts; testes; dashboard e revisão final. O histórico mostra a ordem em que cada parte foi construída.

## Onde a IA errou ou assumiu algo

A IA inicialmente confundiu o aplicativo visual Controle de Gastos com a fonte de dados do pipeline e criou uma integração desnecessária com o formato interno do app. Isso não era o objetivo do trabalho. A correção foi remover essa integração e deixar claro que a **Olist é a fonte real**, enquanto Controle de Gastos é o tema usado para formular as perguntas e os indicadores.

Na validação dos dados, foi conferido que `order_payments` possui várias linhas para o mesmo pedido. Por isso, o pipeline soma as parcelas para obter o gasto do pedido e usa contagens distintas de pedidos. Os testes unitários usam dados inventados e rodam sem abrir o banco do projeto, como exigido.
