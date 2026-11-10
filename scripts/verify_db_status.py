"""Verify DB Tables and Live Call Metadata
"""
import sqlite3
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    conn = sqlite3.connect('data/manuscript.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cursor.fetchall()]
    print("Tables:", tables)

    if "live_api_execution_logs" in tables:
        cursor.execute("""
            SELECT call_id, execution_id, provider, unit_id, is_error, http_status, finish_reason
            FROM live_api_execution_logs
            WHERE call_id = 'LIVE_CALL_001'
        """)
        print("\nLIVE_CALL_001 in live_api_execution_logs:")
        for row in cursor.fetchall():
            print(f"  {row[0]} - {row[1]} - {row[2]} - {row[3]} - error={row[4]} - {row[5]} - {row[6]}")

    if "token_usage_records" in tables:
        cursor.execute("PRAGMA table_info(token_usage_records)")
        cols = [col[1] for col in cursor.fetchall()]
        print("\ntoken_usage_records columns:", cols)
        cursor.execute("""
            SELECT provider, count(*), sum(input_tokens), sum(output_tokens), sum(total_tokens)
            FROM token_usage_records
            GROUP BY provider
        """)
        print("\nToken Usage Summary:")
        for row in cursor.fetchall():
            print(f"  Provider: {row[0]}, Calls: {row[1]}, In: {row[2]}, Out: {row[3]}, Total: {row[4]}")

if __name__ == "__main__":
    main()
