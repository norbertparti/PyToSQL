import yaml

class SQLQueryBuilder:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def select(self, table_name):
        self.query_type = "SELECT"
        self.table_name = table_name
        return self

    def insert(self, table_name):
        self.query_type = "INSERT INTO"
        self.table_name = table_name
        return self

    def update(self, table_name):
        self.query_type = "UPDATE"
        self.table_name = table_name
        return self

    def delete(self, table_name):
        self.query_type = "DELETE FROM"
        self.table_name = table_name
        return self

    def set(self, **kwargs):
        set_str = ", ".join([f"{k} = {v}" for k, v in kwargs.items()])
        self.set_str = set_str
        return self

    def where(self, **kwargs):
        where_str = " AND ".join([f"{k} = {v}" for k, v in kwargs.items()])
        self.where_str = f"WHERE {where_str}"
        return self

    def build(self):
        if self.query_type == "SELECT":
            return f"{self.query_type} * FROM {self.table_name} {self.where_str};"
        elif self.query_type == "INSERT INTO":
            columns = ', '.join(self.config[self.table_name]['columns'])
            values = ', '.join(['%s'] * len(self.config[self.table_name]['columns']))
            return f"{self.query_type} {self.table_name} ({columns}) VALUES({values});"
        elif self.query_type == "UPDATE":
            return f"{self.query_type} {self.table_name} SET {self.set_str} {self.where_str};"
        elif self.query_type == "DELETE FROM":
            return f"{self.query_type} {self.table_name} {self.where_str};"
