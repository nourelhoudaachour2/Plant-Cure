from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import json
import os
from pathlib import Path
from datetime import datetime

from services.recommendation_service import generate_recommendation

app = FastAPI(title="Plant Cure")
app.mount("/static/uploads", StaticFiles(directory="static/uploads"), name="uploads")

HISTORY_FILE = os.getenv("JSON_PATH", "/app/data/history.json")
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model_service:8001")

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def compute_stats(history):
    total = len(history)
    healthy = sum(1 for item in history if item["prediction"]["is_healthy"])
    diseased = total - healthy

    total_savings = 0
    for item in history:
        rec = item.get("recommendation", {})
        org_price = rec.get("traitement_organique", {}).get("prix_estime", 0) or 0
        chim_price = rec.get("traitement_chimique", {}).get("prix_estime", 0) or 0
        if chim_price > org_price:
            total_savings += (chim_price - org_price)

    return {
        "economies_total": round(total_savings, 2),
        "total_predictions": total,
        "plantes_saines": healthy,
        "plantes_malades": diseased
    }


@app.get("/api/stats")
def get_stats():
    history = load_history()
    return compute_stats(history)


@app.get("/api/history")
def get_history():
    history = load_history()
    history = sorted(history, key=lambda x: x["date_analyse"], reverse=True)
    return history


@app.post("/api/analyser")
async def analyser(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{MODEL_SERVICE_URL}/predict",
                files={"file": (file.filename, contents)}
            )
        prediction = response.json()

        recommendation = generate_recommendation(
            prediction["plant"],
            prediction["disease"],
            prediction["is_healthy"]
        )

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        safe_name = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / safe_name

        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        entry = {
            "id": timestamp,
            "image_name": file.filename,
            "image_url": f"/static/uploads/{safe_name}",
            "date_analyse": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "prediction": prediction,
            "recommendation": recommendation
        }

        history = load_history()
        history.append(entry)
        save_history(history)

        return JSONResponse({
            "success": True,
            "data": entry,
            "stats": compute_stats(history)
        })

    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)