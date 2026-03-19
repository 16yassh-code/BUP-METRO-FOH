from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STORE_PATH = DATA_DIR / "project_store.json"

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


def _load_store() -> dict[str, Any]:
    if not STORE_PATH.exists():
        return {"stations": {}, "progress": {}}
    try:
        return json.loads(STORE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"stations": {}, "progress": {}}


def _save_store(data: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STORE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


@app.get("/api/progress")
def get_progress():
    data = _load_store()
    return jsonify(data.get("progress", {}))


@app.get("/api/station/<station>")
def get_station(station: str):
    data = _load_store()
    station_key = station.upper()
    payload = data.get("stations", {}).get(station_key, {})
    return jsonify(payload)


@app.post("/api/station/<station>")
def save_station(station: str):
    body = request.get_json(silent=True) or {}
    station_key = station.upper()

    store = _load_store()
    store.setdefault("stations", {})[station_key] = {
        "tables": body.get("tables", {}),
        "updatedAt": body.get("updatedAt"),
    }

    progress = body.get("progress")
    if isinstance(progress, dict):
        store.setdefault("progress", {})[station_key] = progress

    _save_store(store)
    return jsonify({"ok": True, "station": station_key})


@app.get("/")
def root():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(BASE_DIR, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
