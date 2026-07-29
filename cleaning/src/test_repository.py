from repository import Repository

repo = Repository()

stats = repo.get_dashboard_statistics()

print("===== DASHBOARD STATISTICS =====")
print(stats)
