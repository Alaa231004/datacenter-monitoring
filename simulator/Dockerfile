FROM python:3.12-slim
WORKDIR /app
COPY simulator/ ./simulator/
COPY collector/equipements.json ./collector/equipements.json
WORKDIR /app/simulator
CMD ["python3", "simulator.py"]
