-- #EASY Questions

-- Question 1: Histogram of Tweets

-- solution: 

WITH table_1 AS (
  SELECT *
  FROM tweets
  WHERE EXTRACT(YEAR FROM tweet_date) = 2022
),
table_2 AS (
  SELECT *
  FROM table_1
),
table_3 AS (
  SELECT 
    user_id, 
    COUNT(tweet_id) AS tweet_bucket
  FROM table_2
  GROUP BY user_id
)
SELECT 
  tweet_bucket, 
  COUNT(user_id) AS users_num
FROM table_3
GROUP BY tweet_bucket;


-- Question 2: Data Science Skills

-- solution: 

WITH table_1 AS (
  SELECT 
    *, 
    CASE  
      WHEN skill = 'Python' OR skill = 'Tableau' OR skill = 'PostgreSQL' THEN 1
      ELSE 0
    END AS count
  FROM candidates
),
table_2 AS (
  SELECT 
    candidate_id, 
    SUM(count) AS sum
  FROM table_1
  GROUP BY candidate_id
)
SELECT candidate_id
FROM table_2
WHERE sum = 3;


-- Question 3: Page With No Likes

-- solution: 

WITH table_1 AS (
  SELECT 
    pages.page_id, 
    page_likes.liked_date
  FROM pages 
  LEFT JOIN page_likes 
    ON pages.page_id = page_likes.page_id
),
table_2 AS (
  SELECT page_id
  FROM table_1
  GROUP BY page_id
  HAVING COUNT(liked_date) = 0
  ORDER BY page_id 
)
SELECT *
FROM table_2;


-- Question 4: Unfinished Parts

-- solution: 

SELECT 
  part, 
  assembly_step
FROM parts_assembly
WHERE finish_date IS NULL;


-- Question 5: Laptop vs. Mobile Viewership

-- solution: 

WITH table_1 AS (
  SELECT 
    *, 
    CASE 
      WHEN device_type = 'laptop' THEN 1
      ELSE 0
    END AS laptop, 
    CASE 
      WHEN device_type IN ('tablet', 'phone') THEN 1
      ELSE 0
    END AS mobile
  FROM viewership
)
SELECT 
  SUM(laptop) AS laptop_views, 
  SUM(mobile) AS mobile_views
FROM table_1;

-- Question 6: Average Post Hiatus (Part 1)

-- solution: 


WITH table_1 AS (
  SELECT 
    p1.user_id, 
    p1.post_id, 
    p1.post_content, 
    p1.post_date AS start_date, 
    p2.post_date AS end_date
  FROM posts AS p1 
  JOIN posts AS p2 
    ON p1.user_id = p2.user_id
  WHERE EXTRACT(YEAR FROM p1.post_date) = 2021 
    AND EXTRACT(YEAR FROM p2.post_date) = 2021
),
table_2 AS (
  SELECT 
    user_id, 
    EXTRACT(DAY FROM MAX(end_date) - MIN(start_date)) AS days_between
  FROM table_1
  WHERE start_date != end_date
  GROUP BY user_id
  HAVING EXTRACT(DAY FROM MAX(end_date) - MIN(start_date)) != 0
)
SELECT *
FROM table_2
ORDER BY days_between;

-- Question 7: Teams Power Users

-- solution:



with table_1 as (

select sender_id, count(content) as count_messages
from messages
where extract(month from sent_date)=8 and extract(year from sent_date)=2022
group by sender_id

)

select * 
from table_1
order by count_messages desc
limit 2


--- Question 8: Duplicate Job Listings

--- solution: 


with table_1 AS
(
select count(job_id) as repeated
FROM
job_listings
group by company_id,title,description
having count(job_id)>1
)

select count(repeated) as duplicate_companies
FROM
table_1


--- Question 9: Cities With Completed Trades

--- solution: 


with table_1 AS
(
select city, trades.order_id as order_id
FROM
trades
left join users

on trades.user_id=users.user_id

where status = 'Completed'
)


select city, count(order_id) as total_orders
from table_1
group by city
order by count(order_id) DESC
limit 3

--- Question 10: Average Review Ratings

--- solution: 

select extract(month from submit_date) as mth , product_id as product , round(avg(stars),2) as avg_stars
from reviews
group by extract(month from submit_date), product_id
order by mth,product

--- Question 11: Well Paid Employees

--- solution: 



with table_1 as (

select e1.employee_id, e1.name

FROM
employee as e1

 left join employee as e2

on e1.manager_id=e2.employee_id

where e1.manager_id is not null and e1.salary > e2.salary


)

select *
FROM
table_1


--- Question 12: Final Account Balance

--- solution: 

SELECT
    account_id,
    SUM(
        CASE
            WHEN transaction_type = 'Deposit' THEN amount
            ELSE -amount
        END
    ) AS final_balance
FROM transactions
GROUP BY account_id;

--- Question 13: App Click-through Rate (CTR)

--- solution: 



with table_1 AS
(
select app_id, event_type, count(timestamp) as no_of_imp_clk
FROM
events
where extract(year from timestamp)=2022
group by app_id, event_type
)

, table_2 AS

(
select T1.app_id, T1.event_type as event_click, T1.no_of_imp_clk as click_rate, T2.event_type as event_imp, T2.no_of_imp_clk as imp_rate
from 
table_1 as T1
join 
table_1 as T2

on T1.app_id=T2.app_id

where T1.event_type='click' and T2.event_type='impression'

)


select app_id, round(((click_rate * 100.0 )/imp_rate),2)  as ctr
from 
table_2
order by round(((click_rate * 100.0 )/imp_rate),2) 
