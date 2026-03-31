import duckdb

def load_db():
    con = duckdb.connect()

    con.execute("CREATE TABLE orders AS SELECT * FROM 'data/orders.csv'")
    con.execute("CREATE TABLE products AS SELECT * FROM 'data/products.csv'")
    con.execute("CREATE TABLE aisles AS SELECT * FROM 'data/aisles.csv'")
    con.execute("CREATE TABLE departments AS SELECT * FROM 'data/departments.csv'")
    con.execute("CREATE TABLE order_products AS SELECT * FROM 'data/order_products__prior.csv'")
    con.execute("CREATE TABLE order_products_train AS SELECT * FROM 'data/order_products__train.csv'")
    return con