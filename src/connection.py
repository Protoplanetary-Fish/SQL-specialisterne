import psycopg2
import pandas as pd
import warnings
from colorama import init, Fore

class DatabaseConnection:
    def __init__(self, dbname, user, password, host):
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

    def execute_query(self, query, return_headers = True):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            if cursor.description:
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                if return_headers:
                    return results, column_names
                return results
            self.connection.commit() # Ensure changes are saved
            return [] if not return_headers else ([], [])
    
    def query_to_dataframe(self, query):
        results, col_names = self.execute_query(query)
        return pd.DataFrame(data=results, columns=col_names)


class CRUD:
    init(autoreset=True)
    def __init__(self, dbname, user, password, host):
        self.db = DatabaseConnection(dbname, user, password, host)

    def create_table(self, table_name: str, override_existing_table : bool = False):
        check_query = f"SELECT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public' AND TABLE_NAME = '{table_name}');"
        table_exists = self.db.execute_query(check_query)[0][0][0]
        if table_exists and not override_existing_table:
            print("INFO: The table " + Fore.YELLOW + f"'{table_name}'" + Fore.WHITE + " already exists. If you want to override it, call this function with" + Fore.RED +" override_existing_table=True")
            return
        query = f"CREATE TABLE {table_name} (id int);"
        self.db.execute_query(query, False)
        print(f"Table '{table_name}' checked/created.")

    def add_row_to_table(self, table_name: str, row : list):
        # row is a list of tuples
        # if headers do not exist in table, create them with info print
        query = f"INSERT INTO {table_name} (name, val) VALUES (%s, %s);"
        self.db.execute_query(query)
        print(f"Row added to {table_name}.")