FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-create models directory
RUN mkdir -p /app/models

COPY . .

# Run training script to generate dummy models
RUN python training/train_models.py

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "predictor:app"]
