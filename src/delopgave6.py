from connection import CRUD
import pandas as pd
from decimal import Decimal
import matplotlib.pyplot as plt

if __name__ == "__main__":
    crud = CRUD(
        "northwind",
        "postgres",
        " ",
        "localhost"
    )

    crud.create_table('test_table')
    crud.