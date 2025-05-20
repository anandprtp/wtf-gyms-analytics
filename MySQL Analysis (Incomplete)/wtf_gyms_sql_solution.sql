/*
🔹 Question 1:
Write a query to find the top 3 gyms with the highest total revenue in the most recent month available in the revenue table. 
Return gym name, total revenue, and the corresponding month name."
*/
SELECT 
    g.gym_id,
    g.gym_name,
    r.month_name,
    SUM(r.total_revenue) AS total_revenue
FROM
    gyms g
        JOIN
    revenue r ON g.gym_id = r.gym_id
WHERE
    (r.month , YEAR(r.record_date)) = (SELECT 
            month, YEAR(record_date)
        FROM
            revenue
        ORDER BY record_date DESC
        LIMIT 1)
GROUP BY g.gym_id , g.gym_name, r.month_name
ORDER BY total_revenue DESC
LIMIT 3;



