# This file contains SQL queries


# Below is the sql query to select rates from the prices table. It select puts null if there are less than 3 records for a day
select_prices = """SELECT * FROM (SELECT 
  CASE WHEN COUNT(*) > 3 THEN ROUND(AVG(prices.price), 2) ELSE NULL END AS average_price, 
  day
FROM 
  public.prices 
WHERE 
  prices.price IS NOT NULL 
  and day >= '{date_from}'
  and day <= '{date_to}'
  and orig_code in ('{origin}')
  and dest_code in ('{destination}') 
group by 
  prices.day) as x ORDER by x.day
"""

# below is the query to read regions (They are preloaded in the application)
select_region_slugs = """SELECT * FROM public.regions ORDER BY parent_slug ASC"""


# below is the query to read ports of a parent region
get_slug_ports = (
    """SELECT code FROM public.ports WHERE parent_slug IN ('{parent_slug}')"""
)

# below is the query to read ports codes (They are used for validation purposes)
get_ports_codes = """SELECT code FROM public.ports"""
