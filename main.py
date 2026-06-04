from modules.dns_finder import DNSFinder
from modules.payload_engine import PayloadEngine

def main():
    print("\n=== Termux Network Diagnostic Tool ===")
    target = input("Insira o dominio alvo (ex: google.com): ").strip()

    dns_tool = DNSFinder(target)
    ip_alvo = dns_tool.resolve_a_record()

    print(f"\n[*] Resolvendo DNS para {target}...")
    if ip_alvo:
        print(f"[+] IP Principal: {ip_alvo}")

        print("\n[*] Buscando Subdominios na base crt.sh (Pode demorar)...")
        subdominios = dns_tool.find_subdomains()

        if subdominios:
            print(f"[+] Foram encontrados {len(subdominios)} subdominios. Amostra:")
            for sub in subdominios[:3]:
                print(f"    - {sub}")
        else:
            print("[-] Nenhum subdominio extra listado.")

        print("\n[*] Configurando Payload de Diagnostico HTTP (Porta 80)...")
        # Usamos uma estrutura de requisicao GET padrao estruturada com quebras CRLF
        user_template = "GET / HTTP/1.1[crlf]Host: [host][crlf]User-Agent: [ua][crlf][crlf]"

        engine = PayloadEngine(host=target, port=80)
        raw_payload = engine.generate(user_template)

        print("[+] String Injetada (Debug):")
        print("-" * 40)
        print(raw_payload.decode('utf-8').replace("\r\n", "\\r\\n\n"))
        print("-" * 40)

        print("\n[*] Disparando Socket TCP e aguardando resposta...")
        resposta_servidor = engine.test_connection(raw_payload)

        print("[+] Resposta Bruta Recebida:")
        print("-" * 40)
        # Exibe as primeiras linhas da resposta para nao poluir a tela do telemovel
        linhas_resposta = resposta_servidor.split("\n")
        for linha in linhas_resposta[:8]:
            print(linha.strip())
        print("-" * 40)
    else:
        print("[-] Falha ao resolver o dominio. Verifique a ligacao.")

if __name__ == "__main__":
    main()
