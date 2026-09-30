from data_reader import get_metric

print("CPU :", get_metric("SRV-001", "cpu"))
print("RAM :", get_metric("SRV-001", "ram"))
print("Power :", get_metric("SRV-001", "power"))
print("CPU Temp :", get_metric("SRV-001", "cpu_temperature"))
