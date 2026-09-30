FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir snmpsim pysmi cryptography
CMD sh -c "python3 update_servers.py && python3 run_snmpsim.py"
EXPOSE 11611/udp
