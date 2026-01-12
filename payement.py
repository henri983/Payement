from flask import Flask, request, jsonify
import sqlite3, secrets, string, datetime
from mailjet_rest import Client

app = Flask(__name__)
MAILJET_API_KEY = "..."
MAILJET_SECRET_KEY = "..."
mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

def db():
    conn = sqlite3.connect("db.sqlite3")
        conn.row_factory = sqlite3.Row
            return conn

            def generate_code(length=12):
                alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
                    code = "".join(secrets.choice(alphabet) for _ in range(length))
                        return "-".join(code[i:i+4] for i in range(0, len(code), 4))

                        @app.route("/webhook/payment", methods=["POST"])
                        def webhook_payment():
                            payload = request.json
                                email = payload.get("email")
                                    file_id = payload.get("file_id")

                                        code = generate_code()
                                            expires_at = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()

                                                conn = db()
                                                    conn.execute(
                                                            "INSERT INTO access_codes(email, file_id, code, status, expires_at, created_at) VALUES (?, ?, ?, 'unused', ?, datetime('now'))",
                                                                    (email, file_id, code, expires_at)
                                                                        )
                                                                            conn.commit()

                                                                                data = {
                                                                                      'Messages': [{
                                                                                              "From": {"Email": "support@tondomaine.com", "Name": "Support"},
                                                                                                      "To": [{"Email": email}],
                                                                                                              "Subject": "Votre code d’accès",
                                                                                                                      "HTMLPart": f"""
                                                                                                                                <p>Merci pour votre achat !</p>
                                                                                                                                          <p>Code : <strong>{code}</strong></p>
                                                                                                                                                    <p>Accédez ici : https://tondomaine.com/accesshttps://tondomaine.com/access</a></p>
                                                                                                                                                              <p>Ce code expire le {(datetime.datetime.utcnow() + datetime.timedelta(days=7)).strftime('%d/%m/%Y')}.</p>
                                                                                                                                                                      """
                                                                                                                                                                            }]
                                                                                                                                                                                }
                                                                                                                                                                                    mailjet.send.create(data=data)
                                                                                                                                                                                        return jsonify({"received": True})

                                                                                                                                                                                        @app.route("/api/validate-code", methods=["POST"])
                                                                                                                                                                                        def validate_code():
                                                                                                                                                                                            data = request.json
                                                                                                                                                                                                email = data.get("email")
                                                                                                                                                                                                    code = data.get("code")

                                                                                                                                                                                                        conn = db()
                                                                                                                                                                                                            row = conn.execute(
                                                                                                                                                                                                                    "SELECT * FROM access_codes WHERE email=? AND code=?",
                                                                                                                                                                                                                            (email, code)
                                                                                                                                                                                                                                ).fetchone()

                                                                                                                                                                                                                                    if not row:
                                                                                                                                                                                                                                            return jsonify({"ok": False, "error": "Code invalide"}), 400
                                                                                                                                                                                                                                                if row["status"] != "unused":
                                                                                                                                                                                                                                                        return jsonify({"ok": False, "error": "Code déjà utilisé"}), 400
                                                                                                                                                                                                                                                            if datetime.datetime.fromisoformat(row["expires_at"]) < datetime.datetime.utcnow():
                                                                                                                                                                                                                                                                    return jsonify({"ok": False, "error": "Code expiré"}), 400

                                                                                                                                                                                                                                                                        # Marque comme utilisé
                                                                                                                                                                                                                                                                            conn.execute("UPDATE access_codes SET status='used', used_at=datetime('now') WHERE id=?", (row["id"],))
                                                                                                                                                                                                                                                                                conn.commit()

                                                                                                                                                                                                                                                                                    # Générez une URL présignée via votre stockage (à implémenter)
                                                                                                                                                                                                                                                                                        presigned_url = f"https://cdn.tondomaine.com/files/{row['file_id']}?tmp={secrets.token_hex(24)}"
                                                                                                                                                                                                                                                                                            return jsonify({"ok": True, "url": presigned_url, "expiresIn": 900})
                                                                                                                                                                                                                                                                                            