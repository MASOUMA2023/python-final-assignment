import sqlite3

def start_query_cli():
    conn = sqlite3.connect("database/mlb_history.db")
    cursor = conn.cursor()

    print(" MLB History Query CLI") 
    print("Type your SQL query or 'exit' to quit.")

    while True:
        query = input("SQL> ")
        if query.lower() in ["exit", "quit"]:
            break
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Exception as e:
            print(" Error:", e) 

    conn.close()

if __name__ == "__main__":
    start_query_cli()