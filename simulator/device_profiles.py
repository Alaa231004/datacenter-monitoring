DEVICE_PROFILES = {

    "Server": [
        "cpu",
        "ram",
        "disk",
        "cpu_temperature",
        "motherboard_temperature",
        "fan_speed",
        "power",
        "network_in",
        "network_out",
        "processes",
        "power_supply_status"
    ],

    "Switch": [
        "cpu",
        "memory",
        "temperature",
        "network_in",
        "network_out",
        "active_ports",
        "interface_errors",
        "port_status",
        "power"
    ],

    "Router": [
        "cpu",
        "memory",
        "network_in",
        "network_out",
        "active_routes",
        "temperature",
        "interface_status"
    ],

    "Firewall": [
        "cpu",
        "memory",
        "active_sessions",
        "network_throughput",
        "connections",
        "temperature"
    ],

    "UPS": [
        "battery_level",
        "runtime",
        "input_voltage",
        "output_voltage",
        "frequency",
        "load",
        "power",
        "temperature",
        "battery_status"
    ],

    "Cooling": [
        "supply_temperature",
        "return_temperature",
        "humidity",
        "fan_speed",
        "power",
        "pressure",
        "compressor_status"
    ],

    "PDU": [
        "current",
        "voltage",
        "power",
        "energy",
        "load",
        "temperature"
    ]
}
