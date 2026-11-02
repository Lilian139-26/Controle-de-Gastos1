COPY (
    SELECT category_group,
           category_name,
           COUNT(*) AS launches,
           ROUND(SUM(amount), 2) AS total_spent,
           ROUND(SUM(amount) / SUM(SUM(amount)) OVER (), 4) AS share_of_expenses
    FROM read_csv_auto('__OUTPUT__')
    WHERE expense_type = 'expense'
    GROUP BY category_group, category_name
    ORDER BY total_spent DESC
) TO '__OUTPUT__' (HEADER, DELIMITER ',');
