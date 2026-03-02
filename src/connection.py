import psycopg2

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
        return cursor.fetchall()  # Returns the results of the query