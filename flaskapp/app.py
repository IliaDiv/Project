from flask import Flask, render_template
import socket
import redis
import os

app = Flask(__name__)

# Redis connection settings (from env or defaults)
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Connect to Redis
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True  # return strings instead of bytes
)

@app.route("/")
def home():
    container_name = socket.gethostname()

    try:
        # Example: get a counter value from Redis
        visits = r.incr("visits")
    except Exception as e:
        visits = f"Redis error: {e}"

    return render_template("index.html", container_name=container_name, visits=visits)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
