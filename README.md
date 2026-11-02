# Controle de Gastos — documentação e pipeline do projeto

## Sobre o projeto

O **Controle de Gastos** é um dashboard/planilha para controle financeiro pessoal. A pessoa usuária registra ganhos e despesas, organiza despesas por grupos e acompanha a evolução mensal, o saldo e o impacto de cada compromisso no orçamento.

Este repositório documenta como o projeto foi estruturado e contém um pequeno pipeline analítico reproduzível com dados de demonstração. O pipeline usa o mesmo modelo conceitual do aplicativo: **ganhos, despesas, categorias, meses e saldo**. Nenhum dado pessoal real é versionado aqui.

O aplicativo publicado possui autenticação para proteger os dados de cada usuário. O repositório público contém apenas código, documentação, testes e dados fictícios de exemplo; não contém login, senha, token privado ou dados do Supabase.

## Perguntas que o projeto responde

- Como o total de despesas evolui mês a mês?
- Qual mês concentra o maior gasto?
- Quanto entrou, quanto saiu e qual foi o saldo em cada mês?
- Qual grupo de despesa representa a maior parte do orçamento?
- Quais despesas recorrentes têm maior impacto no total anual?

Não há clientes, pedidos ou vendas neste projeto. O foco é exclusivamente o controle financeiro pessoal.

## Modelo de dados do aplicativo

- **Ganhos:** valores recebidos por mês, com descrição opcional.
- **Cartões:** despesas lançadas por mês em cada cartão.
- **Contas fixas:** compromissos recorrentes, como aluguel, internet e energia.
- **Contas adicionais:** despesas variáveis, como lazer e transporte.
- **Categorias:** agrupamentos usados para comparar o peso de cada tipo de gasto.
- **Saldo mensal:** ganhos do mês menos despesas do mês.

## Camadas do pipeline

1. **Raw** (`data/raw/`): dados de demonstração no formato tabular, preservados como entrada.
2. **Refined** (`data/refined/`): dados tipados, normalizados e ligados à tabela de categorias por `category_id`.
3. **Marts** (`data/marts/`): indicadores prontos para consulta pelo dashboard, sem cálculos de negócio na tela.

O pipeline contém duas tabelas de entrada ligadas por chave: `transactions.csv` e `categories.csv`. Isso permite demonstrar um JOIN sem expor qualquer dado pessoal.

## Indicadores

- `monthly_personal_spending.csv`: despesas, ganhos, saldo e quantidade de lançamentos por mês.
- `category_spend_summary.csv`: total anual, quantidade de lançamentos e participação de cada grupo.
- `recurring_expense_summary.csv`: despesas recorrentes e seu impacto acumulado.

Cada indicador possui um arquivo `.sql` correspondente em `sql/marts/`.

## Como executar

Requisitos: Python 3.10+.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python -m src.run_pipeline
pytest -q
```

Para abrir o dashboard opcional:

```bash
streamlit run dashboard/app.py
```

O dashboard lê somente `data/marts/`. O cálculo acontece antes, no pipeline e nos SQLs.

## Boas práticas utilizadas

- separação entre entrada, transformação e indicadores;
- nenhum dado pessoal ou segredo no Git;
- nomes de campos padronizados;
- valores monetários tratados como números;
- SQL separado por indicador;
- testes unitários com dados inventados, sem abrir o banco do projeto;
- histórico de commits por etapa;
- workflow do GitHub Actions executando os testes;
- autenticação mantida no aplicativo, fora deste repositório analítico.

## Histórico de construção

O projeto foi construído em etapas: documentação e estrutura; modelo de dados de demonstração; transformação e JOIN; indicadores mensais; testes; dashboard e revisão final. O histórico de commits mostra a evolução dessas etapas.

## Onde a IA errou ou assumiu algo

A IA inicialmente desviou o projeto para uma análise de clientes, estados, pedidos e pagamentos da Olist. Isso não representava o Controle de Gastos, que é uma ferramenta de finanças pessoais e não possui clientes. A revisão removeu esse vocabulário e reorganizou o pipeline para trabalhar com ganhos, despesas, categorias, meses e saldo.

A conferência também verificou que os dados de demonstração não são dados da usuária. O projeto público não recebe os valores salvos no aplicativo nem depende de uma conta do Supabase para executar os testes.
