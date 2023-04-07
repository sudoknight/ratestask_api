
-- SELECT * FROM public.regions
-- order by parent_slug;



-- select avg(price) from
-- (SELECT count(*) AS theCount
-- FROM public.prices) as x;



-- calculate avg when the rows of the day are more than 3 else return null
-- SELECT 
-- CASE WHEN COUNT(*) > 3 THEN AVG(prices.price) ELSE NULL END AS avg_column, prices.day, count(*) as count_rows
-- FROM public.prices
-- WHERE prices.price is not NULL
-- group by prices.day;


-- SELECT code FROM public.ports where parent_slug='north_europe_main';

-- SELECT * from prices where day = '2016-01-04';


-- Select NAME, LOCATION, PHONE_NUMBER from DATABASE 
-- WHERE ROLL_NO IN
-- (SELECT ROLL_NO from STUDENT where SECTION=’A’); 


-- SELECT count(slug), parent_slug FROM public.regions
-- WHERE regions.parent_slug IS NOT NULL
-- group by regions.parent_slug 


-- SELECT DISTINCT parent_slug from public.ports

-- SELECT * from  public.ports where parent_slug = 'north_europe_main'
-- or parent_slug='uk_main'

-- SELECT slug, parent_slug FROM public.regions
-- where slug = 'northern_europe' or parent_slug = 'northern_europe'