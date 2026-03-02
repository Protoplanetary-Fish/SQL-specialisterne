select * from orders
where shipcountry = 'Canada'
and extract(year from shippeddate) = 1997
and extract(month from shippeddate) in (1, 2, 3, 4)