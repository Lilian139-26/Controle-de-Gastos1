from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REFINED = ROOT / "data" / "refined"
MARTS = ROOT / "data" / "marts"


def run() -> None:
    REFINED.mkdir(parents=True, exist_ok=True)
    MARTS.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    transactions_path = str(RAW / "transactions.csv").replace("'", "''")
    categories_path = str(RAW / "categories.csv").replace("'", "''")
    con.execute(f"CREATE OR REPLACE VIEW transactions_raw AS SELECT * FROM read_csv_auto('{transactions_path}')")
    con.execute(f"CREATE OR REPLACE VIEW categories_raw AS SELECT * FROM read_csv_auto('{categories_path}')")
    refined = REFINED / "transactions_refined.csv"
    refined_sql = (ROOT / "sql/refined/transactions_refined.sql").read_text()
    con.execute(refined_sql.replace("__OUTPUT__", str(refined).replace("'", "''")))
    marts = [
        ("monthly_personal_spending.sql", "monthly_personal_spending.csv"),
        ("category_spend_summary.sql", "category_spend_summary.csv"),
        ("recurring_expense_summary.sql", "recurring_expense_summary.csv"),
    ]
    for sql_name, output_name in marts:
        sql = (ROOT / "sql/marts" / sql_name).read_text()
        output = MARTS / output_name
        query = sql.replace("__OUTPUT__", str(refined).replace("'", "''"))
        query = query.replace(f"TO '{str(refined).replace(chr(39), chr(39)+chr(39))}'", f"TO '{str(output).replace(chr(39), chr(39)+chr(39))}'")
        con.execute(query)
        print(f"gerado: {output.relative_to(ROOT)}")
    con.close()


if __name__ == "__main__":
    run()
