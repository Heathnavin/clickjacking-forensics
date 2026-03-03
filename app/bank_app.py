from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "evidence")
os.makedirs(LOG_DIR, exist_ok=True)
AUDIT_LOG = os.path.join(LOG_DIR, "audit.log")

def log_event(user_id, action, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | user={user_id} | action={action} | details={details}\n")

@app.route("/")
def home():
    return """
    <html>
      <body style="font-family:Arial; padding:30px;">
        <h2>FinPortal Dashboard</h2>
        <p>Welcome to your account.</p>
        <a href="/transfer?user=100&amount=500">
          <button style="padding:10px 18px; font-size:16px;">Transfer $300</button>
        </a>
      </body>
    </html>
    """

@app.route("/transfer")
def transfer():
    user_id = request.args.get("user", "unknown")
    amount = request.args.get("amount", "0")
    log_event(user_id, "transfer", f"amount={amount}")
    return f"""
    <html>
      <body style="font-family:Arial; padding:30px;">
        <h2>Transfer Recorded</h2>
        <p>User {user_id} initiated transfer of ${amount}.</p>
        <a href="/">Back to dashboard</a>
      </body>
    </html>
    """

@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none';"
    return response

if __name__ == "__main__":
    app.run(port=5000, debug=True)