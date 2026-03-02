from connection import DatabaseConnection

db = DatabaseConnection(
    "northwind",
    "postgres",
    " ",
    "localhost"
)


results = db.execute_query("SELECT * FROM products LIMIT 5;")

print(results)