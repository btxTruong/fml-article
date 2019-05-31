import psycopg2


class PostgreSQL:
    def __init__(self, params):
        self.params = params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.params)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()




