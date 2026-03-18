from fastapi import FastAPI

app = FastAPI(title="Universal Province Engine")

@app.get("/")
def read_root():
    return {"message": "Sengoku Engine is breathing."}

@app.get("/province/izu")
def get_izu_status():
    return {
        "province": "伊豆",
        "status": "alive",
        "composite_score": 100,
        "population": 10
    }