COPY (
    SELECT description,
           category_group,
           COUNT(*) AS months_with_charge,
           ROUND(SUM(amount), 2) AS total_spent
    FROM read_csv_auto('__OUTPUT__')
    WHERE expense_type = 'expense' AND is_recurring = true
    GROUP BY description, category_group
    ORDER BY total_spent DESC
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
