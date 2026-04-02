from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os, re, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app,
                default_limits=["100 per minute"])

SECRET_KEY = os.getenv("SECRET_KEY", "")

NAME_REGEX = re.compile(r"^[a-zA-Z0-9 ]{1,50}$")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/greet", methods=["POST"])
def greet():
    data = request.get_json(silent=True)
    if not data or "name" not in data:
        return jsonify({"error": "name required"}), 400
    name = str(data["name"]).strip()
    if not NAME_REGEX.match(name):
        return jsonify({"error": "invalid name"}), 400
    logger.info("Greeting: %s", name)
    return jsonify({"message": f"Hello, {name}!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)