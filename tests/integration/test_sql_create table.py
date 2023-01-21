"""Tesing the SQLQueryBuilder class with Table creation and data insertion"""

from PyToSQL.SQLBuilder import SQLQueryBuilder

import sqlite3
import yaml

def test_sql_query_builder():
    # Create a test database
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    # Create the tables in the database
    with open('tests/integration/create_table.yaml', 'r') as f:
        config = yaml.safe_load(f)
        for table_name, table_config in config.items():
            columns = ', '.join([f"{column} {'INTEGER' if column == 'id' else 'VARCHAR(255)'}" for column in table_config['columns']])
            primary_key = f"PRIMARY KEY({table_config['primary_key']})"
            if 'foreign_keys' in table_config:
                foreign_keys = ', '.join([f"FOREIGN KEY({column}) REFERENCES {ref}" for column, ref in table_config['foreign_keys'].items()])
                command = f"CREATE TABLE {table_name} ({columns}, {primary_key}, {foreign_keys});"
            else:
                command = f"CREATE TABLE {table_name} ({columns}, {primary_key});"
            c.execute(command)

    # Insert test data into the users table
    builder = SQLQueryBuilder("tests/integration/create_table.yaml")
    query = builder.insert("users").build()
    insert1 = query % ("John Doe", "john@example.com", "password")
    insert2 = query %  ("Jane Smith", "jane@example.com", "password")
    c.execute(insert1)
    c.execute(insert2)


    # Test a SELECT query
    query = builder.select("users").where(id=1).build()
    c.execute(query)
    result = c.fetchone()
    assert result == (1, "John Doe", "john@example.com", "password")
    conn.close()
