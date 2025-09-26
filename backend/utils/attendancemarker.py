import json
import hashlib
from datetime import datetime
import psycopg2
import os
import sys

# Ensure config import works
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_NAME, DB_HOST, DB_PORT, SAN_PASS

# DB connection helper
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user="santhosh_user",
        password=SAN_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

# Validate QR payload and mark attendance
def mark_attendance(student_id: int, qr_payload: str, geo_location=None, photo_hash=None):
    """
    student_id : user_id of the student scanning the QR
    qr_payload : JSON string scanned from QR
    geo_location : optional, string
    photo_hash : optional, string
    """
    try:
        # Decode QR JSON
        data = json.loads(qr_payload)
        session_id = data.get("session_id")
        token = data.get("token")
        issued_at = data.get("issued_at")

        # Recompute token to verify
        raw = f"{session_id}_{issued_at}_SAS_SECRET_KEY"
        expected_token = hashlib.sha256(raw.encode()).hexdigest()
        if token != expected_token:
            print("❌ Invalid QR token")
            return False

        # Insert attendance record
        conn = get_db_connection()
        cur = conn.cursor()

        # Optional: prevent duplicate attendance
        cur.execute("""
            SELECT * FROM attendance_records
            WHERE user_id=%s AND session_id=%s
        """, (student_id, session_id))
        if cur.fetchone():
            print("⚠ Attendance already marked")
            cur.close()
            conn.close()
            return True

        cur.execute("""
            INSERT INTO attendance_records (user_id, session_id, timestamp, geo_location, photo_hash)
            VALUES (%s, %s, %s, %s, %s)
        """, (student_id, session_id, datetime.utcnow(), geo_location, photo_hash))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Attendance marked successfully")
        return True

    except Exception as e:
        print("❌ Error:", e)
        return False

# Test Example
if __name__ == "__main__":
    # Example: simulate a scanned QR
    # Use an integer session_id that exists in your DB, e.g., 1
    session_id = 1
    issued_at = "2025-09-27T10:30:00Z"
    token = hashlib.sha256(f"{session_id}_{issued_at}_SAS_SECRET_KEY".encode()).hexdigest()
    qr_example = json.dumps({
        "session_id": session_id,
        "issued_at": issued_at,
        "token": token
    })
    mark_attendance(student_id=1, qr_payload=qr_example, geo_location="12.34,56.78", photo_hash="hash123")