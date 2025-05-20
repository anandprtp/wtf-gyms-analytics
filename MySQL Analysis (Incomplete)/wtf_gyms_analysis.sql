USE wtf_gyms_latest;

-- 🔁 Retention & Membership Trends
-- 1. What is the total number of active members in each gym?
SELECT 
    g.gym_id,
    g.gym_name,
    COUNT(DISTINCT m.member_id) AS active_members
FROM
    gyms g
        LEFT JOIN
    members m ON g.gym_id = m.gym_id
        LEFT JOIN
    subscriptions s ON m.member_id = s.member_id
WHERE
    s.status = 'active'
GROUP BY g.gym_id , g.gym_name
ORDER BY active_members DESC;


-- Retention Rate = (Members who stayed this month ÷ Members at the start of the month) × 100
-- 2. What is the monthly member retention rate for each gym?



-- 3. Which age group has the highest membership retention?


-- 💸 Revenue, Cost & Profitability
-- 1. What is the total revenue and total operating cost per gym?

-- 2. Which gyms are profitable and which are not? (Revenue - CTO)

-- 3. What is the average revenue per member by gym and by plan type?

-- 4. What is the LTV (lifetime value) of a customer by plan type?

-- 🧍‍♂️ Employee & Sales Insights
-- 1. Which employees added the most members in the last 6 months?

-- 2. Which employees have the highest retention rate for the members they onboarded?

-- 3. What is the average number of members assigned per employee in each gym?

-- 📊 Plan Performance
-- 1. Which membership plan type generates the highest revenue across all gyms?

-- 2. What is the distribution of plan type sales per gym?

-- 3. What is the churn rate per plan type (based on expired vs renewed subscriptions)?

-- 📍 City & Gym Performance
-- 1. Which city is generating the most revenue?

-- 2. Which gym has the highest ROI (Revenue ÷ CTO)?


/*
"Write a query to find the top 3 gyms with the highest total revenue in the most recent month available in the revenue table. 
Return gym name, total revenue, and the corresponding month name."
*/
SELECT 
    g.gym_id,
    g.gym_name,
    r.month_name,
    SUM(r.total_revenue) AS total_revenue
FROM
    gyms g
        LEFT JOIN
    revenue r ON g.gym_id = r.gym_id
WHERE
    (r.month , YEAR(r.record_date)) = (SELECT 
            month, YEAR(record_date)
        FROM
            revenue
        ORDER BY record_date DESC
        LIMIT 1)
GROUP BY g.gym_id , g.gym_name , r.month_name
ORDER BY total_revenue DESC
LIMIT 3;

