CREATE TABLE IF NOT EXISTS metrics (

    id SERIAL PRIMARY KEY,

    equipment_id VARCHAR(50),
    hostname VARCHAR(100),
    type VARCHAR(50),

    timestamp TIMESTAMP,

    cpu FLOAT,
    ram FLOAT,
    disk FLOAT,

    temperature FLOAT,
    power FLOAT,

    network_in FLOAT,
    network_out FLOAT,

    fan_speed INTEGER,

    status VARCHAR(20),

    risk_level VARCHAR(20),

    collection_source VARCHAR(50),

    processed_at TIMESTAMP,

    processed_by VARCHAR(50),

    review_status VARCHAR(20),

    review_comment TEXT,

    anomaly_count INTEGER
);
