COPY (
    SELECT month,
           ROUND(SUM(CASE WHEN expense_type = 'expense' THEN amount ELSE 0 END), 2) AS expenses,
           ROUND(SUM(CASE WHEN expense_type = 'income' THEN amount ELSE 0 END), 2) AS income,
           COUNT(*) AS launches,
           ROUND(SUM(CASE WHEN expense_type = 'income' THEN amount ELSE -amount END), 2) AS balance
    FROM read_csv_auto('__OUTPUT__')
    GROUP BY month
    ORDER BY month
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
