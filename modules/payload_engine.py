class PayloadEngine:
    def __init__(self, host, port, proxy_host=None):
        self.host = host
        self.port = str(port)
        self.proxy_host = proxy_host or host

    def get_standard_tags(self):
        return {
            "[host]": self.host,
            "[port]": self.port,
            "[proxy]": self.proxy_host,
            "[crlf]": "\r\n",
            "[ua]": "Mozilla/5.0 (Android; Mobile; rv:100.0)",
        }

    def generate(self, template_string):
        payload = template_string
        for tag, value in self.get_standard_tags().items():
            payload = payload.replace(tag, value)
        return payload.encode('utf-8')
