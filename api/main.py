from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="Universal Province Engine")

BASE_URL = "https://raw.githubusercontent.com/otspace0715/hex-shogun-map/main/sengoku_hex_data_v2"

PROVINCES = [
    "伊豆", "相模", "武蔵", "安房", "上総", "下総", "常陸",
    "山城", "大和", "河内", "和泉", "摂津", "伊賀", "伊勢",
    "志摩", "尾張", "三河", "遠江", "駿河", "甲斐", "信濃",
    "飛弾", "美濃", "近江", "越前", "加賀", "能登", "越中",
    "越後", "佐渡", "丹波", "丹後", "但馬", "因幡", "伯耆",
    "出雲", "石見", "隠岐", "播磨", "美作", "備前", "備中",
    "備後", "安芸", "周防", "長門", "紀伊", "淡路", "阿波",
    "讃岐", "伊予", "土佐", "筑前", "筑後", "豊前", "豊後",
    "肥前", "肥後", "日向", "大隅", "薩摩", "壱岐", "対馬",
    "上野", "下野", "陸奥", "出羽", "若狭"
]


@app.get("/")
def read_root():
    return {"message": "Sengoku Engine is breathing."}


@app.get("/provinces")
def list_provinces():
    return {"provinces": sorted(PROVINCES), "count": len(PROVINCES)}


@app.get("/province/{name}")
def get_province(name: str):
    if name not in PROVINCES:
        raise HTTPException(status_code=404, detail=f"{name} not found")

    url = f"{BASE_URL}/{name}.json"
    r = httpx.get(url, timeout=10.0)

    if r.status_code != 200:
        raise HTTPException(status_code=404, detail=f"{name} data not found")

    data = r.json()
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
            ),
        },
    }