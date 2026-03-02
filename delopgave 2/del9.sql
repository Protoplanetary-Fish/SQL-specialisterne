select * from orders
where employeeid in (2, 5, 8)
and shipregion is not null
and shipvia in (1, 3)
order by employeeid, shipvia asc