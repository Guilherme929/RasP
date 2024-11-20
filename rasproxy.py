#!/usr/bin/env python3
import requests 
import sys
from fake_useragent import UserAgent
import os
import random
import time

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
            print('proxies salvo com sucesso.\n')
            print('em: RasP/proxies.txt')
        except Exception as erro:
            print('Ops! Ocorreu um erro: {}'.format(erro))
    
    def verificando(self, pasta, arquivo):
        caminho = os.path.join(pasta, arquivo)
        
        os.makedirs(pasta, exist_ok=True)

        try:
            if os.path.exists(caminho):
                os.remove(caminho)
                time.sleep(1)
                proxies = self.colentando_proxies()
                self.salvando_proxies(proxies, caminho)
                print('Prontinho atualizamos sua lista de proxies ;)')
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

    def help(self):
        print("""Menu:
Author: (https://github.com/Guilherme929)

Olá, aqui é o Guilherme ;)

Essa ferramenta consiste em coletar proxies de um site (json), e salvar em uma pasta,
e uma arquivos expecífico: RasP/proxies.txt 
              """)
if __name__ == '__main__':
    web = WebScreper()

    '''Essa parte, é a configuração dos arquivos, e pastas.'''
    pasta = "RasP"
    arquivo = "proxies.txt"
    
    if ('-h') in sys.argv:
        web.help()
        sys.exit(0)

    web.verificando(pasta, arquivo)
    pergunta = input('Você deseja abrir a lista de proxies s/n: ')

    if pergunta in ('s', 'S'):
        web.abrir_arquivo(os.path.join(pasta, arquivo))
    
