from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
REFINED = ROOT / "data" / "refined"
MARTS = ROOT / "data" / "marts"


def csv(name: str) -> str:
    return str(RAW / name)


def run() -> None:
    REFINED.mkdir(parents=True, exist_ok=True)
    MARTS.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect()
    con.execute(f"CREATE OR REPLACE VIEW orders_raw AS SELECT * FROM read_csv_auto('{csv('olist_orders_dataset.csv')}', header=true)")
    con.execute(f"CREATE OR REPLACE VIEW payments_raw AS SELECT * FROM read_csv_auto('{csv('olist_order_payments_dataset.csv')}', header=true)")
    con.execute(f"CREATE OR REPLACE VIEW customers_raw AS SELECT * FROM read_csv_auto('{csv('olist_customers_dataset.csv')}', header=true)")
    con.execute("CREATE OR REPLACE TABLE refined_orders AS SELECT * FROM orders_raw")
    con.execute("CREATE OR REPLACE TABLE refined_payments AS SELECT * FROM payments_raw")
    con.execute("CREATE OR REPLACE TABLE refined_customers AS SELECT * FROM customers_raw")
    for sql_file, output in [
        (ROOT / 'sql/refined/order_spend.sql', REFINED / 'order_spend.csv'),
        (ROOT / 'sql/refined/customer_spend.sql', REFINED / 'customer_spend.csv'),
        (ROOT / 'sql/marts/monthly_spend_by_state.sql', MARTS / 'monthly_spend_by_state.csv'),
        (ROOT / 'sql/marts/payment_method_mix.sql', MARTS / 'payment_method_mix.csv'),
        (ROOT / 'sql/marts/customer_spend_profile.sql', MARTS / 'customer_spend_profile.csv'),
    ]:
        query = sql_file.read_text()
        target = str(output).replace("'", "''")
        if 'marts/' in str(output):
            input_refined = str(REFINED / 'customer_spend.csv').replace("'", "''")
            query = query.replace("read_csv_auto('__OUTPUT__')", f"read_csv_auto('{input_refined}')")
        con.execute(query.replace("__OUTPUT__", target))
        print(f"gerado: {output.relative_to(ROOT)}")
    con.close()


if __name__ == '__main__':
    run()
