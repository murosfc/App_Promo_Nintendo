import sys
import Ferramentas
import ManipularDB
import time

lidos = 0

#inicia cores
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

#classe para manipular valores a salvar do BD
class dados_dos_jogos:
    def __init__(self):
        self.nsuid = ''
        self.titulo = ''
        self.msrp = '' # msrp = Manufacturer's Suggested Retail Price
        self.sale_price = ''
        self.validade_promo = ''
        self.url_img = ''
    pass

#faz a leitura de dados no site da Nintendo
def scraping_nintendo(tipo_extracao, driver):
    #DBapp = ManipularDB.iniciar_db()
    Ferramentas.abrir_botoes_mais(driver)
    indice = 1
    total_itens = Ferramentas.conta_itens(driver)

    if (tipo_extracao == 1):
        sys.stdout.write(RED)
        ManipularDB.limpa_db_antiga(tipo_extracao)
        print('\nIniciando a leitura de promoções no site da Nintendo Brasil. Aguarde')
        sys.stdout.write(RESET)
    else:
        sys.stdout.write(RED)
        if (tipo_extracao == 0):
            print('\nLeitura de A-Z')
        else:
            print('\nLeitura de Z-A')
        print('\nIniciando a leitura completa do site da Nintendo Brasil. Aguarde...')
        sys.stdout.write(RESET)

    dados_jogo_lido = dados_dos_jogos()
    while True:
        try:
            driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
        except Exception:
            if tipo_extracao == 0:
                '''lê os jogos novamente do final para o inicio para garantir 100% de leitura'''
                driver.quit()
                tipo_extracao = 3
                driver = Ferramentas.iniciar_navegador(tipo_extracao)
                # executa a leitura e gravação dos dados obtido no site da nintendo
                scraping_nintendo(tipo_extracao, driver)
            elif tipo_extracao == 3:
                tipo_extracao = 1
                inicio2 = time.time()
                driver.quit()
                driver = Ferramentas.iniciar_navegador(tipo_extracao)
                # executa a leitura e gravação dos dados obtido no site da nintendo
                quantidade_itens_promo = scraping_nintendo(tipo_extracao, driver)
                print("\nTempo gasto para leitura das promoções", "{:.0f}".format((time.time() - inicio2)), "segundos")
            else:
                sys.stdout.write(GREEN)
                print (f'\n\nQuantidade de jogos em promoção {indice - 1}')
                sys.stdout.write(RESET)
            return (indice - 1)  # encerra o scrapping caso não encontre mais jogos e retorna a quantidade de jogos em promoção
        if tipo_extracao == 1: #atualização de promo
            dados_jogo_lido.nsuid = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('nsuid')
            dados_jogo_lido.titulo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
            dados_jogo_lido.sale_price = Ferramentas.trata_preco(driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('sale-price'))
            dados_jogo_lido.validade_promo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('date')
            dados_jogo_lido.msrp = Ferramentas.trata_preco(driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('msrp'))
            dados_jogo_lido.url_img = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('image')
            #Grava na DB principal os não exibidos pelo limite do site inicial
            ManipularDB.gravar_db(dados_jogo_lido, tipo_extracao)  # grava dados lido na DB
        else: #atualização completa
            dados_jogo_lido.nsuid = driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('nsuid')
            dados_jogo_lido.titulo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
            dados_jogo_lido.msrp = Ferramentas.trata_preco(driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('msrp'))
            dados_jogo_lido.url_img = driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('image')
            ManipularDB.gravar_db(dados_jogo_lido, tipo_extracao)  # grava dados lido na DB
        Ferramentas.imprime_avanco(indice, total_itens)
        indice += 1




