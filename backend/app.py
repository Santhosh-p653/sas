from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "sas_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "santhosh_user")  # admin user for app
DB_PASS = os.getenv("SAN_USER_PASS", "1234")

# Flask app configuration
app = Flask(
    __name__,
    template_folder="../app/pages",  # HTML templates
    static_folder="../app"           # CSS, JS, assets
)
app.secret_key = "supersecretkey"   # session management key, change in production

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]

        # Student: no username/password
        if role == "student":
            username = f"student_{role}"  # optional identifier
            session["username"] = username
            session["role"] = "student"
            flash("Logged in as student!", "success")
            return redirect(url_for("student_dashboard"))

        # Teacher/Admin/Auditor: username & password required
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Please enter username and password!", "danger")
            return redirect(url_for("login"))

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s;",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session["username"] = username
            session["role"] = user[0]
            flash("Login successful!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid username or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Student dashboard
@app.route("/student")
def student_dashboard():
    if "role" in session and session["role"] == "student":
        return render_template("student.html", username=session["username"])
    flash("Please login first.", "danger")
    return redirect(url_for("login"))

# Admin/Teacher/Auditor dashboard
@app.route("/admin")
def admin_dashboard():
    if "role" in session and session["role"] in ["admin", "teacher", "auditor"]:
        return render_template(
            "admin.html",
            username=session["username"],
            role=session["role"]
        )
    flash("Access denied! Please login.", "danger")
    return redirect(url_for("login"))

# Logout
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
