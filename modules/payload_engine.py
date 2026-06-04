import socket

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

    def test_connection(self, raw_payload, timeout=5):
        """
        Abre um socket TCP nativo, envia os bytes do payload 
        e captura o retorno estruturado do servidor ou do proxy.
        """
        try:
            # Cria o socket para IPv4 (AF_INET) e fluxo TCP (SOCK_STREAM)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)

            # Inicia a conexao de rede na porta especificada
            sock.connect((self.host, int(self.port)))

            # Envia todos os bytes da string injetada
            sock.sendall(raw_payload)

            # Captura os primeiros 1024 bytes da resposta (suficiente para ler os cabecalhos)
            response = sock.recv(1024)
            sock.close()

            return response.decode('utf-8', errors='ignore')
        except socket.timeout:
            return "[-] Erro: Tempo limite de conexao esgotado (Timeout)."
        except Exception as e:
            return f"[-] Erro critico na conexao: {str(e)}"
