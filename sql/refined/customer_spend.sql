COPY (
    SELECT c.customer_id, c.customer_unique_id, c.customer_city, c.customer_state,
           o.order_id, CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchased_at,
           strftime(CAST(o.order_purchase_timestamp AS TIMESTAMP), '%Y-%m') AS order_month,
           o.order_status, COALESCE(SUM(p.payment_value), 0) AS order_paid_value,
           COALESCE(MAX(p.payment_installments), 0) AS payment_installments
    FROM customers_raw c
    JOIN orders_raw o USING (customer_id)
    LEFT JOIN payments_raw p USING (order_id)
    GROUP BY ALL
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
