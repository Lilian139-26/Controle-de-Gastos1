COPY (
    SELECT customer_unique_id, customer_state,
           COUNT(DISTINCT order_id) AS orders,
           ROUND(SUM(order_paid_value), 2) AS total_paid,
           ROUND(SUM(order_paid_value) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS avg_ticket,
           MIN(purchased_at) AS first_purchase, MAX(purchased_at) AS last_purchase
    FROM read_csv_auto('__OUTPUT__')
    GROUP BY customer_unique_id, customer_state
    ORDER BY total_paid DESC
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
