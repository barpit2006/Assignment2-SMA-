import pandas as pd
import os
import pymysql

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'directory_scraper')
}

def export_to_csv():
    conn = pymysql.connect(**DB_CONFIG)
    query = "SELECT * FROM extracted_architects"
    df = pd.read_sql(query, conn)
    df.to_csv("data/dataset_snapshot.csv", index=False)
    print("✅ Exported dataset snapshot to data/dataset_snapshot.csv")
    conn.close()

if __name__ == "__main__":
    export_to_csv()
