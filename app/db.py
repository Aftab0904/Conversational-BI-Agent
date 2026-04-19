import duckdb
import os

def load_db():
    con = duckdb.connect()

    # Get the path to the data folder relative to this script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    con.execute(f"CREATE TABLE orders AS SELECT * FROM '{os.path.join(data_dir, 'orders.csv')}'")
    con.execute(f"CREATE TABLE products AS SELECT * FROM '{os.path.join(data_dir, 'products.csv')}'")
    con.execute(f"CREATE TABLE aisles AS SELECT * FROM '{os.path.join(data_dir, 'aisles.csv')}'")
    con.execute(f"CREATE TABLE departments AS SELECT * FROM '{os.path.join(data_dir, 'departments.csv')}'")
    con.execute(f"CREATE TABLE order_products AS SELECT * FROM '{os.path.join(data_dir, 'order_products__prior.csv')}'")
    con.execute(f"CREATE TABLE order_products_train AS SELECT * FROM '{os.path.join(data_dir, 'order_products__train.csv')}'")
    return con