import json
import os
import sys
import mysql.connector
from dotenv import load_dotenv

def main():
    # Check CLI args
    if len(sys.argv) < 2:
        print("Usage: python src/import_holdings.py <path-to-holdings.json>")
        sys.exit(1)

    json_file = sys.argv[1]

    # Load environment variables
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # Connect to DB
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cur = conn.cursor()

    # Clear old snapshot
    cur.execute("DELETE FROM holding_meta")
    cur.execute("DELETE FROM holdings")

    # Load JSON
    with open(json_file) as f:
        data = json.load(f)

    # Insert holdings + meta
    for h in data:
        cur.execute("""
            INSERT INTO holdings (asset_name, asset_type, institution, current_value, currency, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            h["asset_name"],
            h["asset_type"],
            h.get("institution"),
            h["current_value"],
            h.get("currency", "INR"),
            h["updated_at"]
        ))
        holding_id = cur.lastrowid

        for key, val in h.get("meta", {}).items():
            json_value = json.dumps(val, ensure_ascii=False)
            cur.execute("""
                INSERT INTO holding_meta (holding_id, meta_key, meta_value)
                VALUES (%s, %s, %s)
            """, (holding_id, key, json_value))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Imported {len(data)} holdings from {json_file}")

if __name__ == "__main__":
    main()
