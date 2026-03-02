select * from orders 
where orderdate >= '19960101' and orderdate <= '19961231'
and shipcountry = 'Germany' 
and employeeid = 1 
and freight >= 100
and shipregion is null