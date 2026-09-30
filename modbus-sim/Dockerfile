FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pymodbus==3.6.9
CMD ["python3", "modbus_server.py"]
EXPOSE 5020
