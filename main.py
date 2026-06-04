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

        print("\n[*] Buscando Subdominios na base crt.sh (Pode demorar alguns segundos)...")
        subdominios = dns_tool.find_subdomains()

        if subdominios:
            print(f"[+] Foram encontrados {len(subdominios)} subdominios. Listando amostra:")
            # Mostra apenas os 5 primeiros para manter o terminal limpo
            for sub in subdominios[:5]:
                print(f"    - {sub}")
            if len(subdominios) > 5:
                print(f"    - ... e mais {len(subdominios) - 5} ocultos.")
        else:
            print("[-] Nenhum subdominio extra encontrado ou tempo limite esgotado.")

        print("\n[*] Configurando Payload Customizado...")
        user_template = "CONNECT [host]:443 HTTP/1.1[crlf]Host: [host][crlf]User-Agent: [ua][crlf][crlf]"

        engine = PayloadEngine(host=target, port=443)
        raw_payload = engine.generate(user_template)

        print("[+] Payload String (Formatado para Debug):")
        print("-" * 40)
        print(raw_payload.decode('utf-8').replace("\r\n", "\\r\\n\n"))
        print("-" * 40)
    else:
        print("[-] Falha ao resolver o dominio. Verifique a conexao ou a escrita.")

if __name__ == "__main__":
    main()
