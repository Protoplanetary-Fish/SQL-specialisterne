from connection import DatabaseConnection
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    db = DatabaseConnection(
        "northwind",
        "postgres",
        " ",
        "localhost"
    )
    orderdetails = db.query_to_dataframe(
        """
        SELECT * FROM orderdetails;
        """
    )
    orders = db.query_to_dataframe(
        """
        SELECT * FROM orders;
        """
    )
    products = db.query_to_dataframe(
        """
        SELECT * FROM products;
        """
    )
    categories = db.query_to_dataframe(
        """
        SELECT * FROM categories;
        """
    )

    orderdetails['order_value'] = orderdetails['unitprice'].astype(
        float) * orderdetails['quantity'].astype(float) * (float(1.0) - orderdetails['discount'].astype(float))

    data = pd.merge(orderdetails, orders, on='orderid')
    data = pd.merge(data, products, on='productid')
    data = pd.merge(data, categories, on='categoryid')

    sales_per_country = data.groupby('shipcountry')[
        'order_value'].sum().sort_values(ascending=False)
    print(sales_per_country)
    sales_per_country.plot.bar()
    plt.xticks(rotation=45, ha='right')
    plt.show()

    sales_per_customer = data.groupby(
        'customerid')['order_value'].sum().sort_values(ascending=False)
    print(sales_per_customer)
    sales_per_customer.plot.box()
    plt.xticks(rotation=45, ha='right')
    plt.show()

    # Plot sales per product category as well as number of products in category
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Subplot 1: Total Sales Value
    sales_per_category = data.groupby('categoryname')[
        'order_value'].sum().sort_values(ascending=False)
    sales_per_category.plot(
        kind='bar', ax=ax1, color='skyblue', edgecolor='black')

    ax1.set_title('Total Sales Value by Category', fontweight='bold')
    ax1.set_ylabel('Total Sales ($)')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    products_in_category = data.groupby(
        'categoryname')['productid'].nunique().reindex(sales_per_category.index)
    products_in_category.plot(
        kind='bar', ax=ax2, color='salmon', edgecolor='black')

    ax2.set_title('Unique Product Count by Category', fontweight='bold')
    ax2.set_ylabel('Number of Unique Products')
    ax2.set_xlabel('Product Category')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
