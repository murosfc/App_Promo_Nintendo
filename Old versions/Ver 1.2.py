'''
Ver. 0.1 Criação do Scrapping em 20/05/2021
Ver. 1.0 Adicionado a extração do nsuid (identificador único do título) e interação com mysql 21/05/2021
Ver. 1.1 Mudanças na abordagem de limpar dados antigos da DB 22/05/2021 resumindo 3 funções em apenas 1
Ver. 1.2 Utilizando a atualização de DB, não mais o conceito de apagar e criar nova.
'''

from selenium import webdriver
import time
import mysql.connector
import sys

Ver = "1.2"

class dados_dos_jogos:
    def __init__(self):
        self.nsuid = ''
        self.titulo = ''
        self.msrp = '' # msrp = Manufacturer's Suggested Retail Price
        self.sale_price = ''
        self.validade_promo = ''
        self.url_img = ''
    pass

def iniciar_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abricó",
        database="db_apppromonintendo"
    )
    print(mydb)
    return mydb

#limpa as promos antigas
def limpa_db_antiga(tipo_extracao, DBapp):
    meucursor = DBapp.cursor()
    if tipo_extracao == 1: #atualização de promo apenas
        meucursor.execute("DROP table jogos_em_promo")  # limpa a base antiga de promoções
        meucursor.execute(
            'CREATE TABLE Jogos_em_promo (DB_Nintendo_BR_nsuid VARCHAR(15) NOT NULL, sale_price FLOAT, validade_promo TEXT, FOREIGN KEY (DB_Nintendo_BR_nsuid) REFERENCES DB_Nintendo_BR(nsuid))')
        DBapp.commit()

def iniciar_navegador(tipo_extracao):
    if tipo_extracao == 1: #atualização de promo
        link = "https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q=&dFR[generalFilters][0]=Deals"
    else: #full update
        link = 'https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q='
    driver = webdriver.Chrome()
    driver.get(link)
    driver.minimize_window()
    return driver

#imprime a % de jogos lidos
def imprime_avanco(i, max):
    sys.stdout.write('\r')
    sys.stdout.write("[%-40s] %d%%" % ('=' * int(i/(max/40)), (100/max * i)))
    #sys.stdout.write("%d%%" % (100/max * i))
    sys.stdout.flush()

#grava dados lidos no banco de dados
def gravar_db (DBapp, dados_jogo_lido, tipo_extracao):
    meucursor =DBapp.cursor()
    if tipo_extracao == 1: #grava promos
        comando = ("INSERT INTO Jogos_em_promo VALUES (%s,%s,%s)")
        valores = (dados_jogo_lido.nsuid, dados_jogo_lido.sale_price, dados_jogo_lido.validade_promo)
        meucursor.execute(comando, valores)
        DBapp.commit()
    else: #grava todos os jogos
        comando = ("INSERT INTO db_nintendo_br VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE img_url=%s") #atualiza os já existentes somente insere os novos
        valores = (dados_jogo_lido.nsuid,dados_jogo_lido.titulo,dados_jogo_lido.msrp,dados_jogo_lido.url_img,dados_jogo_lido.url_img)
        meucursor.execute (comando, valores)
        DBapp.commit()

#retira caracteres de R$ do preço e converte para 0 valores inválidos
def trata_preco(preco):
    #print (preco)
    if preco == 'Gratuito' or preco == None:
        preco = 0.00;
    else:
        preco = preco.replace('R$ ', '')
        preco = preco.replace(',','.')
    return preco

#faz a leitura de dados no site da Nintendo
def scraping_nintendo(DBapp, tipo_extracao):
    indice = 1
    total_itens = int ((driver.find_element_by_xpath ('//*[@id="result-count"]').text).replace (' resultados','')) #armazena quantos itens disponíveis para leitura
    dados_jogo_lido = dados_dos_jogos()
    while True:
        try:
            driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
        except Exception:
            if tipo_extracao == 0:
                sys.stdout.write(GREEN)
                print (f'\nJogos disponível segundo o site da Nitendo {total_itens}')
                print (f'Lidos {indice-1} jogos do site da Nintendo BR')
                sys.stdout.write(RESET)
            return (indice - 1)  # encerra o scrapping caso não encontre mais jogos e retorna a quantidade de jogos em promoção
        try:
            driver.find_element_by_id("btn-load-more").click()  # clica no botão para carregar mais
            time.sleep(0.5)
        except Exception:
            pass
        if tipo_extracao == 1: #atualização de promo
            dados_jogo_lido.nsuid = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('nsuid')
            dados_jogo_lido.sale_price = trata_preco(driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('sale-price'))
            dados_jogo_lido.validade_promo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('date')
            gravar_db (DBapp, dados_jogo_lido, tipo_extracao) #grava dados lido na DB
        else: #atualização completa
            dados_jogo_lido.nsuid = driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('nsuid')
            dados_jogo_lido.titulo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
            dados_jogo_lido.msrp = trata_preco(driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('msrp'))
            dados_jogo_lido.url_img = driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('image')
            gravar_db(DBapp, dados_jogo_lido, tipo_extracao)  # grava dados lido na DB
        imprime_avanco(indice, total_itens)
        indice += 1


############# PROGRAMA PRINCIPAL #################
#inicia cores
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

DBapp = iniciar_db()
inicio = time.time()
tipo_extracao = 0 #enviar 1 para promoções e 0 atualização completa
driver = iniciar_navegador(tipo_extracao)
if (tipo_extracao == 1):
    limpa_db_antiga(tipo_extracao, DBapp)
    sys.stdout.write(RED)
    print('\n\nIniciando a leitura de promoções no site da Nintendo Brasil. Aguarde')
    sys.stdout.write(RESET)
    quantidade_itens_promo = scraping_nintendo(DBapp,
                                               tipo_extracao)  # executa a leitura e gravação dos dados obtido no site da nintendo
else:
    sys.stdout.write(RED)
    print('\n\nIniciando a leitura do site da Nintendo Brasil. Aguarde...')
    sys.stdout.write(RESET)
    scraping_nintendo(DBapp, tipo_extracao)  # executa a leitura e gravação dos dados obtido no site da nintendo
    print("Tempo gasto para leitura completa", "{:.2f}".format((time.time() - inicio) / 60), "minutos")
    tipo_extracao = 1
    sys.stdout.write(RED)
    inicio2 = time.time()
    print('\nIniciando a leitura de promoções no site da Nintendo Brasil. Aguarde...')
    sys.stdout.write(RESET)
    driver.quit()
    driver = iniciar_navegador(tipo_extracao)
    quantidade_itens_promo = scraping_nintendo(DBapp, tipo_extracao)  # executa a leitura e gravação dos dados obtido no site da nintendo
    print("\nTempo gasto para leitura das promoções", "{:.0f}".format((time.time() - inicio2)), "segundos")
    sys.stdout.write(RESET)
sys.stdout.write(GREEN)
print(f'\nQuantidade de itens em promoção {quantidade_itens_promo}')
sys.stdout.write(RESET)
sys.stdout.write(CYAN)
print('\n\nPrograma finalizado')
sys.stdout.write(RESET)
print("Tempo total gasto para processar", "{:.2f}".format((time.time() - inicio)/60), "minutos")
driver.quit()