-- #EASY Questions

-- Question 1: Histogram of Tweets

-- solution: 

with table_1 as
(
select *
from tweets
where EXTRACT(YEAR from tweet_date)=2022
) ,
table_2 AS
(
select *
FROM
table_1
)
, table_3 as
(
select user_id, count(tweet_id) as tweet_bucket
from table_2
group by user_id
)

select tweet_bucket , count(user_id) as users_num
from table_3
group by tweet_bucket 


-- Question 2: Data Science Skills

-- solution: 


with table_1 as (

select * , 

(
case  
when skill='Python' or skill='Tableau' or skill='PostgreSQL' then 1
else 0
end
) as count
from candidates

)

,

table_2 AS
(
select candidate_id, sum(count)
from table_1
group by candidate_id
)

select candidate_id
FROM table_2
where sum=3


-- Question 3: Page With No Likes

-- solution: 


with table_1 as 
(

select pages.page_id, liked_date
from pages left join page_likes
on pages.page_id=page_likes.page_id

)
,

table_2 AS
(
select page_id
FROM table_1
group by page_id
having count(liked_date)=0
order by page_id 
)


SELECT *
FROM
TABLE_2


-- Question 4: Unfinished Parts

-- solution: 

