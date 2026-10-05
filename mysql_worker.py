import time
import random
import os
import pymysql

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'directory_scraper'),
    'autocommit': True
}

def get_next_task(cursor):
    """Fetch and lock the next pending task."""
    cursor.execute(
        """
        SELECT record_id FROM crawl_queue 
        WHERE status = 'pending' OR (status = 'failed' AND attempts < 3)
        ORDER BY updated_at ASC LIMIT 1
        """
    )
    row = cursor.fetchone()
    if row:
        record_id = row[0]
        cursor.execute(
            "UPDATE crawl_queue SET status = 'in_progress' WHERE record_id = %s",
            (record_id,)
        )
        return record_id
    return None

def process_record(record_id):
    """Simulate parsing and data extraction."""
    # 95% simulated success rate to demonstrate error handling
    if random.random() < 0.05:
        raise Exception("Simulated connection timeout / 503 error")

    return {
        "record_id": record_id,
        "full_name": f"Architect Sample_{record_id.split('/')[-1]}",
        "registration_no": record_id,
        "state": random.choice(["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu"]),
        "address": "Sample Street, Suite 101",
        "valid_upto": "2030-12-31",
        "source_url": f"https://example.com/view?id={record_id}"
    }

def run_pipeline():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("🚀 Starting Resumable MySQL Worker Loop...")

    while True:
        record_id = get_next_task(cursor)
        if not record_id:
            print("✅ All queue items processed!")
            break

        print(f"⏳ Processing task: {record_id}...")
        try:
            data = process_record(record_id)
            
            # Save extracted record
            cursor.execute(
                """
                INSERT INTO extracted_architects 
                (record_id, full_name, registration_no, state, address, valid_upto, source_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE full_name=VALUES(full_name)
                """,
                (data['record_id'], data['full_name'], data['registration_no'],
                 data['state'], data['address'], data['valid_upto'], data['source_url'])
            )

            # Mark completed
            cursor.execute(
                "UPDATE crawl_queue SET status = 'completed' WHERE record_id = %s",
                (record_id,)
            )
            print(f"  ✓ Saved: {record_id}")

        except Exception as e:
            print(f"  ❌ Failed: {record_id} | Reason: {e}")
            cursor.execute(
                """
                UPDATE crawl_queue 
                SET status = 'failed', attempts = attempts + 1, last_error = %s 
                WHERE record_id = %s
                """,
                (str(e), record_id)
            )

        # Politeness delay with jitter
        time.sleep(random.uniform(0.5, 1.5))

    # Print Dashboard Summary
    cursor.execute("SELECT status, COUNT(*) FROM crawl_queue GROUP BY status")
    print("\n--- Pipeline Summary ---")
    for status, count in cursor.fetchall():
        print(f"  {status.upper()}: {count}")

    conn.close()

if __name__ == "__main__":
    run_pipeline()
