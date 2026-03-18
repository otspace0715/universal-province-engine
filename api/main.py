from fastapi import FastAPI, HTTPException
import json
import os

app = FastAPI(title="Universal Province Engine")

DATA_DIR = "data/hex-shogun-map/sengoku_hex_data_v2"

def load_province(name: str):
    path = os.path.join(DATA_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"{name} not found")
    with open(path, encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def read_root():
    return {"message": "Sengoku Engine is breathing."}

@app.get("/provinces")
def list_provinces():
    files = os.listdir(DATA_DIR)
    provinces = [f.replace(".json", "") for f in files if f.endswith(".json")]
    return {"provinces": sorted(provinces), "count": len(provinces)}

@app.get("/province/{name}")
def get_province(name: str):
    data = load_province(name)
    cells = data["cells"]
    passable = [c for c in cells if c["attr"]["passable"]]
    flat = [c for c in cells if c["attr"]["terrain_type"] == 0]
    mountain = [c for c in cells if c["attr"]["terrain_type"] == 2]
    has_coastal = any(c["attr"]["elevation_m"] == 0 for c in cells)
    return {
        "province": name,
        "status": "alive",
        "terrain": {
            "total_cells": len(cells),
            "passable_cells": len(passable),
            "flat_cells": len(flat),
            "mountain_cells": len(mountain),
            "has_coastal": has_coastal,
            "avg_elevation_m": round(
                sum(c["attr"]["elevation_m"] for c in cells) / len(cells), 1
            )
        }
    }