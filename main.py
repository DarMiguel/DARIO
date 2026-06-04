import argparse
import sys
from modules.dns_finder import DNSFinder
from modules.payload_engine import PayloadEngine

# Definindo cores ANSI para o Termux
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def print_banner():
    print(f"{Colors.CYAN}")
    print("==========================================")
    print("   TERMUX NETWORK DIAGNOSTIC TOOL v1.0    ")
    print("==========================================\n")
    print(f"{Colors.RESET}")

def main():
    # Configurando a leitura de argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Ferramenta de diagnostico de rede e firewall para Termux.")
    parser.add_argument("-t", "--target", required=True, help="Dominio alvo (ex: google.com)")
    parser.add_argument("-p", "--port", type=int, default=80, help="Porta alvo (padrao: 80)")

    # Se o usuario rodar apenas 'python main.py', mostra o menu de ajuda e sai
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    print_banner()
    target = args.target
    port = args.port

    print(f"{Colors.YELLOW}[*] Iniciando diagnostico para: {target} (Porta: {port}){Colors.RESET}")

    dns_tool = DNSFinder(target)
    ip_alvo = dns_tool.resolve_a_record()

    if not ip_alvo:
        print(f"{Colors.RED}[-] Erro critico: Falha ao resolver o dominio {target}.{Colors.RESET}")
        sys.exit(1)

    print(f"{Colors.GREEN}[+] IP Principal resolvido: {ip_alvo}{Colors.RESET}")

    print(f"\n{Colors.YELLOW}[*] Buscando subdominios na base crt.sh...{Colors.RESET}")
    subdominios = dns_tool.find_subdomains()

    if subdominios:
        print(f"{Colors.GREEN}[+] Encontrados {len(subdominios)} subdominios. Amostra:{Colors.RESET}")
        for sub in subdominios[:3]:
            print(f"    - {sub}")
    else:
        print(f"{Colors.RED}[-] Nenhum subdominio extra listado ou falha na busca.{Colors.RESET}")

    print(f"\n{Colors.YELLOW}[*] Gerando Payload e disparando Socket TCP...{Colors.RESET}")
    user_template = "GET / HTTP/1.1[crlf]Host: [host][crlf]User-Agent: [ua][crlf][crlf]"

    engine = PayloadEngine(host=target, port=port)
    raw_payload = engine.generate(user_template)

    resposta_servidor = engine.test_connection(raw_payload)

    print(f"\n{Colors.GREEN}=== RESPOSTA DO SERVIDOR ==={Colors.RESET}")
    linhas = resposta_servidor.split('\n')
    for linha in linhas[:8]:  # Mostra apenas as primeiras 8 linhas da resposta
        print(linha.strip())
    print(f"{Colors.GREEN}============================{Colors.RESET}")

if __name__ == "__main__":
    main()
