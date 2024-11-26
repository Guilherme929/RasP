#!/usr/bin/env python3
import requests 
import sys
from fake_useragent import UserAgent
import os
import time
from tqdm import tqdm

class WebScreper:
    def __init__(self):
        self.fake_header = {"User-Agent": UserAgent().random}
        
    def colentando_proxies(self):
        try:
            response = requests.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json", headers=self.fake_header)
            response.raise_for_status()
            time.sleep(1)

            proxy_json = response.json()
            coluna_proxy = proxy_json.get("proxies")

            if not coluna_proxy:
                print('Programa não conseguiu encontrar proxies.')
                return

            proxies = [proxy["proxy"].strip() for proxy in coluna_proxy if "proxy" in proxy]
            return proxies
        except requests.exceptions.RequestException as erro:
            print('Ops! Ocorreu um erro: \n')
            print(f'{erro}')

    def salvando_proxies(self, proxies, caminho):
        if not proxies:
            print('programa não conseguiu salvar proxies.')
            return

        try:
            with open(caminho, 'a') as file:
                for proxy in proxies:
                    file.write(f"{proxy}\n")
            print('Proxies salvos com sucesso.')
            print('Em: RasP/proxies.txt\n')
        except Exception as erro:
            print(f'Ops! Ocorreu um erro: {erro}')
    
    def verificando(self, pasta, arquivo):
        caminho = os.path.join(pasta, arquivo)
        
        os.makedirs(pasta, exist_ok=True)

        try:
            if os.path.exists(caminho):
                os.remove(caminho)
                time.sleep(1)
                proxies = self.colentando_proxies()
                self.salvando_proxies(proxies, caminho)
                print('Prontinho! Atualizamos sua lista de proxies ;)')
            elif not os.path.exists(caminho):
                proxies = self.colentando_proxies()
                self.salvando_proxies(proxies, caminho)
                print('Salvamos sua lista de proxies.')
        except Exception as error:
            print(f'Ops! Ocorreu um erro: {error}')
    
    def abrir_arquivo(self, caminho):
        try:
            with open(caminho, 'r') as file:
                print('Lista de proxies: \n\n')
                for line in file:
                    print(line.strip()) 
        except Exception as erro:
            print(f'Ops! Ocorreu um erro: {erro}')

    def verificar_proxies(self, proxies):
        valid_proxies = []
        print("Verificando proxies...\n")
        
        # Usando tqdm para mostrar uma barra de progresso
        for i in tqdm(range(0, len(proxies), 5), desc="Testando proxies", unit="grupo de 5"):
            proxy_group = proxies[i:i+5]  # Pegando blocos de 5 proxies
            for proxy in proxy_group:
                try:
                    test_url = "https://httpbin.org/ip"
                    proxy_dict = {"http": f"http://{proxy}", "https": f"https://{proxy}"}
                    response = requests.get(test_url, proxies=proxy_dict, timeout=5)
                    
                    if response.status_code == 200:
                        valid_proxies.append(proxy)
                except requests.exceptions.RequestException:
                    pass

            # Exibir a tela novamente a cada 5 proxies testados
            time.sleep(0.5)  # Pausa de 0.5s entre as verificações para "animar"

        print("\nVerificação completa.")
        return valid_proxies

    def help(self):
        print("""Menu:
Author: (https://github.com/Guilherme929)

Olá, aqui é o Guilherme ;)

Essa ferramenta consiste em coletar proxies de um site (json), e salvar em uma pasta,
e um arquivo específico: RasP/proxies.txt 

Não se preocupe em apagar o 'proxies.txt' para atualizar sua lista de proxies, o script já faz isso automaticamente, assim
que se inicia o script
""")
        
if __name__ == '__main__':
    web = WebScreper()

    pasta = "RasP"
    arquivo = "proxies.txt"
    
    if ('-h') in sys.argv:
        web.help()
        sys.exit(0)

    web.verificando(pasta, arquivo)

    try:
        pergunta = input('\nVocê deseja abrir a lista de proxies? (s/n): ')
        if pergunta in ('s', 'S'):
            web.abrir_arquivo(os.path.join(pasta, arquivo))
        
        pergunta = input("\nDeseja verificar os proxies agora? (s/n): ")
        if pergunta in ('s', 'S'):
            # Carregando proxies do arquivo
            with open(os.path.join(pasta, arquivo), 'r') as file:
                proxies = [line.strip() for line in file]
            
            valid_proxies = web.verificar_proxies(proxies)
            if valid_proxies:
                print("\nProxies válidos encontrados:")
                for proxy in valid_proxies:
                    print(proxy)
            else:
                print("\nNenhum proxy válido encontrado.")
    except Exception:
        print('Ops! Algo ocorreu fora de contexto!')
        print('Por favor, tente novamente!\n')

