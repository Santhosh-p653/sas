import qrcode
import json
import hashlib
from datetime import datetime
import psycopg2
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import DB_NAME, DB_HOST, DB_PORT, SAN_PASS
# ...existing code...

# DB Connection Helper
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user="santhosh_user",
        password=SAN_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def generate_qr(session_id: str):
    # Create secure token
    timestamp = datetime.utcnow().isoformat()
    raw_data = f"{session_id}_{timestamp}_SAS_SECRET_KEY"
    token = hashlib.sha256(raw_data.encode()).hexdigest()

    # Data to embed
    payload = {
        "session_id": session_id,
        "issued_at": timestamp,
        "token": token
    }
    qr_data = json.dumps(payload)

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Save to assets folder
    assets_dir = os.path.join(os.path.dirname(__file__), "assets/qr_codes")
    os.makedirs(assets_dir, exist_ok=True)
    filename = f"qr_{session_id}.png"
    filepath = os.path.join(assets_dir, filename)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)



    # Save to DB
    conn = get_db_connection()
    cur = conn.cursor()
    with open(filepath, "rb") as f:
        qr_bytes = f.read()
        cur.execute("""
            INSERT INTO qr_codes (session_id, qr_image)
            VALUES (%s, %s)
        """, (session_id, psycopg2.Binary(qr_bytes)))
    conn.commit()
    cur.close()
    conn.close()

    return filepath


if __name__ == "__main__":
    path = generate_qr("CS101")
    print(f"QR generated and saved at: {path}")