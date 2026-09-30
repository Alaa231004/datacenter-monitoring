class Equipment:

    def __init__(
        self,
        id,
        hostname,
        type,
        location,
        manufacturer,
        model,
        protocol=None,
        ip=None,
        port=None,
        community=None,
        slave_id=None
    ):
        self.id = id
        self.hostname = hostname
        self.type = type
        self.location = location
        self.manufacturer = manufacturer
        self.model = model

        # Communication
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.community = community
        self.slave_id = slave_id

    def __str__(self):
        return (
            f"{self.hostname} | "
            f"{self.type} | "
            f"{self.protocol} | "
            f"{self.location}"
        )
