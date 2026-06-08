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
