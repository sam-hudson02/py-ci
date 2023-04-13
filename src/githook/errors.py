class invalidRequest(Exception):
    def __init__(self, reason, ip):
        self.message = reason
        self.ip = ip

class invalidPayload(Exception):
    def __init__(self, reason, ip):
        self.message = reason
        self.ip = ip