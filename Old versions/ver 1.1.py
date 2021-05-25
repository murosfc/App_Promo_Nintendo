'''
Ver. 0.1 Criação do Scrapping em 20/05/2021
Ver. 1.0 Adicionado a extração do nsuid (identificador único do título) e interação com mysql 21/05/2021
Ver. 1.1 Mudanças na abordagem de limpar dados antigos da DB 22/05/2021 resumindo 3 funções em apenas 1
'''

from selenium import webdriver
import time
import mysql.connector

Ver = "0.2"

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
        password="root",
        database="db_apppromonintendo"
    )
    print(mydb)
    return mydb

def iniciar_navegador(tipo_extracao):
    if tipo_extracao == 1: #atualização de promo
        link = "https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q=&dFR[generalFilters][0]=Deals"
    else: #full update
        link = 'https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q='
    driver = webdriver.Chrome()
    driver.get(link)
    driver.minimize_window()
    return driver

def limpa_db_antiga(tipo_extracao, DBapp):
    meucursor = DBapp.cursor()
    if tipo_extracao == 1: #atualização de promo apenas
        meucursor.execute("DROP table jogos_em_promo")  # limpa a base antiga de promoções
        meucursor.execute(
            'CREATE TABLE Jogos_em_promo (DB_Nintendo_BR_nsuid VARCHAR(15) NOT NULL, sale_price FLOAT, validade_promo TEXT, FOREIGN KEY (DB_Nintendo_BR_nsuid) REFERENCES DB_Nintendo_BR(nsuid))')
        DBapp.commit()
    else: #full update
        meucursor.execute("DROP table jogos_em_promo")  # limpa a base antiga de promoções
        meucursor.execute("DROP table DB_Nintendo_BR")  # limpa base de jogos
        meucursor.execute(
            'CREATE TABLE DB_Nintendo_BR (nsuid VARCHAR(15) NOT NULL, titulo TEXT, msrp FLOAT, img_url TEXT, PRIMARY KEY(nsuid))')
        DBapp.commit()
        meucursor.execute(
            'CREATE TABLE Jogos_em_promo (DB_Nintendo_BR_nsuid VARCHAR(15) NOT NULL, sale_price FLOAT, validade_promo TEXT, FOREIGN KEY (DB_Nintendo_BR_nsuid) REFERENCES DB_Nintendo_BR(nsuid))')
        DBapp.commit()

def gravar_db (DBapp, dados_jogo_lido, tipo_extracao):
    meucursor =DBapp.cursor()
    if tipo_extracao == 1: #grava promos
        comando = ("INSERT INTO Jogos_em_promo VALUES (%s,%s,%s)")
        valores = (dados_jogo_lido.nsuid, dados_jogo_lido.sale_price, dados_jogo_lido.validade_promo)
        meucursor.execute(comando, valores)
        DBapp.commit()
    else: #grava todos os jogos
        comando = ("INSERT INTO db_nintendo_br VALUES (%s,%s,%s,%s)")
        valores = (dados_jogo_lido.nsuid,dados_jogo_lido.titulo,dados_jogo_lido.msrp,dados_jogo_lido.url_img)
        meucursor.execute (comando, valores)
        DBapp.commit()

def trata_preco(preco):
    print (preco)
    if preco == 'Gratuito' or preco == None:
        preco = 0.00;
    else:
        preco = preco.replace('R$ ', '')
        preco = preco.replace(',','.')
    return preco

def scraping_nintendo(DBapp, tipo_extracao):
    indice = 1
    dados_jogo_lido = dados_dos_jogos()
    while True:
        try:
            driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
        except Exception:
            if tipo_extracao == 0:
                print (f'Lidos {indice} jogos do site da Nintendo BR')
            return (indice - 1)  # encerra o scrapping caso não encontre mais jogos e retorna a quantidade de jogos em promoção
        try:
            driver.find_element_by_id("btn-load-more").click()  # clica no botão para carregar mais
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
        indice += 1


# programa principal
DBapp = iniciar_db()
inicio = time.time()
tipo_extracao = 0 #enviar 1 para promoções e 0 atualização completa
limpa_db_antiga(tipo_extracao, DBapp) #limpa a db antiga para uma nova ser gravada
print('Iniciando a leitura do site da Nintendo Brasil. Aguarde')
driver = iniciar_navegador(tipo_extracao)
quantidade_itens_promo = scraping_nintendo(DBapp, tipo_extracao)  # executa a leitura e gravação dos dados obtido no site da nintendo
if (tipo_extracao == 0):
    tipo_extracao = 1
    print('Iniciando a leitura de promoçõe no site da Nintendo Brasil. Aguarde')
    driver = iniciar_navegador(tipo_extracao)
    quantidade_itens_promo = scraping_nintendo(DBapp, tipo_extracao)  # executa a leitura e gravação dos dados obtido no site da nintendo
print(f'quantidade de itens em promoção {quantidade_itens_promo}')
print('Programa finalizado')
print("Tempo gasto para processar", time.time() - inicio)

