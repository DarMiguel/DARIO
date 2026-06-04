import socket

class DNSFinder:
    def __init__(self, target_domain):
        self.target = target_domain

    def resolve_a_record(self):
        try:
            return socket.gethostbyname(self.target)
        except socket.gaierror:
            return None
