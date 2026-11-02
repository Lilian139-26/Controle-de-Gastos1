COPY (
    SELECT t.transaction_id, t.month, t.category_id,
           c.category_name, c.category_group, t.expense_type,
           t.description, CAST(t.amount AS DOUBLE) AS amount,
           CAST(t.is_recurring AS BOOLEAN) AS is_recurring
    FROM transactions_raw t
    JOIN categories_raw c USING (category_id)
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
