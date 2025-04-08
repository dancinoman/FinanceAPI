import sqlite3

class sqlite:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table (self, table_name, columns):
        """
        Create a table in the database.
        :param table_name: Name of the table to create.
        :param columns: Dictionary of column names and their data types.
        """
        columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")
        self.connection.commit()
