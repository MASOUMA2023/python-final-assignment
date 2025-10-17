import sqlite3
import pandas as pd

conn = sqlite3.connect("database/mlb_history.db")

df = pd.read_sql_query("SELECT * FROM mlb_history LIMIT 5;", conn)

print("First 5 rows from mlb_history table:")
print(df)

conn.close()
