import time
import logging
from flask import Flask, render_template, request, jsonify
from config import SCREEN_W, SCREEN_H, BG, FG
from simulator import Simulator

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

sim = Simulator()                 # the whole phone lives here, in Python
last_time = time.perf_counter()


@app.route("/")
def index():
    cfg = {"w": SCREEN_W, "h": SCREEN_H, "bg": BG, "fg": FG}
    return render_template("index.html", cfg=cfg)


@app.route("/api/frame", methods=["POST"])
def api_frame():
    global last_time
    data = request.get_json(silent=True) or {}
    now = time.perf_counter()
    dt = min(now - last_time, 0.05)
    last_time = now
    frame = sim.step(data.get("pressed", []), set(data.get("held", [])), dt)
    return jsonify(frame=frame)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)