FROM python:3.12-slim

WORKDIR /gameclubbooking

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

COPY backend/ .


CMD ["sh", "-c", "alembic upgrade d1ac0b8e13ca && alembic upgrade head && uvicorn src.app:app --host 0.0.0.0 --port 8080"]
