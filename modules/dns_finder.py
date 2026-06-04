import socket
import urllib.request
import json

class DNSFinder:
    def __init__(self, target_domain):
        self.target = target_domain

    def resolve_a_record(self):
        try:
            return socket.gethostbyname(self.target)
        except socket.gaierror:
            return None

    def find_subdomains(self):
        """
        Consulta a API publica crt.sh para encontrar subdominios passivamente.
        Retorna uma lista limpa e sem duplicados.
        """
        url = f"https://crt.sh/?q=%25.{self.target}&output=json"
        subdomains = set() # Usamos 'set' para evitar dominios repetidos

        try:
            # Simulamos um navegador (User-Agent) para a API nao bloquear o Termux
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))

                for entry in data:
                    name = entry.get('name_value', '')
                    # Limpa quebras de linha e o asterisco (*.) dos certificados curinga
                    for sub in name.split('\n'):
                        sub = sub.replace('*.', '').strip()
                        if sub.endswith(self.target):
                            subdomains.add(sub)

            return sorted(list(subdomains))
        except Exception:
            # Retorna lista vazia caso o site nao responda a tempo
            return []
