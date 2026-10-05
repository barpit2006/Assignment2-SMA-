import os
import pymysql

# Update with your local MySQL credentials
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'directory_scraper'),
    'autocommit': True
}

def generate_queue_seeds(count=100):
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print(f"Seeding MySQL database with {count} task IDs...")

    for i in range(1, count + 1):
        record_id = f"CA/2026/{i:05d}"
        cursor.execute(
            "INSERT IGNORE INTO crawl_queue (record_id, status) VALUES (%s, 'pending')",
            (record_id,)
        )

    print("✅ Seed generation complete!")
    conn.close()

if __name__ == "__main__":
    generate_queue_seeds(100)
