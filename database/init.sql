CREATE TABLE server_metrics (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER,
    hostname VARCHAR(50),
    timestamp TIMESTAMP,

    cpu FLOAT,
    ram FLOAT,
    disk FLOAT,

    temperature FLOAT,
    power FLOAT,

    network_in FLOAT,
    network_out FLOAT,

    fan_speed FLOAT,

    status VARCHAR(20),
    risk_level VARCHAR(20),

    collection_source VARCHAR(50),
    processed_at TIMESTAMP,
    processed_by VARCHAR(50),

    review_status VARCHAR(50),
    review_comment TEXT
);


CREATE TABLE ups_metrics (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER,
    hostname VARCHAR(50),
    timestamp TIMESTAMP,

    battery_level FLOAT,
    runtime FLOAT,

    input_voltage FLOAT,
    output_voltage FLOAT,

    frequency FLOAT,
    load FLOAT,

    power FLOAT,
    temperature FLOAT,

    status VARCHAR(20),
    risk_level VARCHAR(20),

    collection_source VARCHAR(50),
    processed_at TIMESTAMP,
    processed_by VARCHAR(50),

    review_status VARCHAR(50),
    review_comment TEXT
);


CREATE TABLE cooling_metrics (
    id SERIAL PRIMARY KEY,
    equipment_id INTEGER,
    hostname VARCHAR(50),
    timestamp TIMESTAMP,

    supply_temperature FLOAT,
    return_temperature FLOAT,

    humidity FLOAT,

    fan_speed FLOAT,

    power FLOAT,

    pressure FLOAT,

    status VARCHAR(20),
    risk_level VARCHAR(20),

    collection_source VARCHAR(50),
    processed_at TIMESTAMP,
    processed_by VARCHAR(50),

    review_status VARCHAR(50),
    review_comment TEXT
);
