COPY (
    SELECT payment_type, COUNT(DISTINCT order_id) AS orders,
           ROUND(SUM(payment_value), 2) AS total_paid,
           ROUND(SUM(payment_value) / SUM(SUM(payment_value)) OVER (), 4) AS value_share,
           ROUND(AVG(payment_installments), 2) AS avg_installments
    FROM payments_raw
    GROUP BY payment_type
    ORDER BY total_paid DESC
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
