# backend/config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

SAN_PASS = os.getenv("SAN_USER_PASS")
NIV_PASS = os.getenv("NIV_USER_PASS")
TIL_PASS = os.getenv("TIL_USER_PASS")
SHR_PASS = os.getenv("SHR_USER_PASS")
