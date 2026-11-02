COPY (
    SELECT
        o.order_id,
        o.customer_id,
        CAST(o.order_purchase_timestamp AS TIMESTAMP) AS purchased_at,
        CAST(CAST(o.order_purchase_timestamp AS TIMESTAMP) AS DATE) AS purchased_date,
        strftime(CAST(o.order_purchase_timestamp AS TIMESTAMP), '%Y-%m') AS order_month,
        o.order_status,
        COALESCE(SUM(p.payment_value), 0) AS order_paid_value,
        COALESCE(MAX(p.payment_installments), 0) AS payment_installments
    FROM orders_raw o
    LEFT JOIN payments_raw p USING (order_id)
    GROUP BY ALL
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
