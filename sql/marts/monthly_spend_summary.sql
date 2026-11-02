COPY (
    SELECT order_month,
           COUNT(DISTINCT order_id) AS orders,
           COUNT(DISTINCT customer_unique_id) AS active_customers,
           ROUND(SUM(order_paid_value), 2) AS total_paid,
           ROUND(SUM(order_paid_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS avg_ticket
    FROM read_csv_auto('__OUTPUT__')
    GROUP BY order_month
    ORDER BY order_month
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
