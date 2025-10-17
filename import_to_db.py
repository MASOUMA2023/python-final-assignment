import sqlite3
import pandas as pd
import os

def import_csv_to_db():
    db_path = "database/mlb_history.db"
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    csv_path = "raw-data/mlb_history.csv"
    if not os.path.exists(csv_path):
        print(f" CSV file not found: {csv_path}")
        return
    
    for file in os.listdir("raw-data"): 
        if file.endswith(".csv"):
            table_name = file.replace(".csv", "")
            csv_path = os.path.join("raw-data", file) 

            df = pd.read_csv(csv_path)
            if df.empty:
                print(" CSV file is empty. Aborting import.")
                return
    

            df.to_sql(table_name, conn, if_exists='replace', index=False)
            print(f" Imported {file} into table {table_name}") 

    conn.close()

if __name__ == "__main__":
    import_csv_to_db()
