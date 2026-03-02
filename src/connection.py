import psycopg2
import pandas as pd

class DatabaseConnection:
    def __init__(self, dbname, user, password, host):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]  # type: ignore
        return results, column_names
    
    def query_to_dataframe(self, query):
        results, col_names = self.execute_query(query)
        return pd.DataFrame(data=results, columns=col_names)