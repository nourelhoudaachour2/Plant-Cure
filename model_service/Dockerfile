FROM python:3.11-slim

WORKDIR /app

COPY model_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY model_service/main.py .
COPY model_service/predict.py .
COPY model/plant_disease_prediction_model.keras /app/model/plant_disease_prediction_model.keras

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]