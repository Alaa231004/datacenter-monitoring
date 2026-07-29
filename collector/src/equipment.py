class Equipment:

    def __init__(
        self,
        id,
        hostname,
        type,
        location,
        manufacturer,
        model
    ):
        self.id = id
        self.hostname = hostname
        self.type = type
        self.location = location
        self.manufacturer = manufacturer
        self.model = model

    def __str__(self):
        return (
            f"{self.hostname} | "
            f"{self.type} | "
            f"{self.location} | "
            f"{self.manufacturer} {self.model}"
        )
