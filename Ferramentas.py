#Ferramentas gerais

from selenium import webdriver
import time
import sys

#inicia cores
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

def iniciar_navegador(tipo_extracao):
    if tipo_extracao == 1: #atualização de promo
        link = "https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q=&dFR[generalFilters][0]=Deals"
    elif tipo_extracao == 0: #full update A-Z
        link = 'https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q=&indexName=ncom_game_pt_br_title_asc'
    else: #full update Z-A
        link = 'https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q=&indexName=ncom_game_pt_br_title_des'
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


#retira caracteres de R$ do preço e converte para 0 valores inválidos
def trata_preco(preco):
    if preco == 'Gratuito' or preco == None:
        preco = 0.00;
    else:
        preco = preco.replace('R$ ', '')
        preco = preco.replace(',','.')
    return preco

def abrir_botoes_mais(driver):
    sys.stdout.write(GREEN)
    start = time.time()
    print ('\nAbrindo os botões de "carregar mais"')
    while True:
        try:
            driver.find_element_by_id("btn-load-more").click()  # clica no botão para carregar mais
            time.sleep(0.5)
        except Exception:
            sys.stdout.write(BOLD)
            print('Botões "carregar mais" abertos em', "{:.0f}".format((time.time() - start)), "segundos")
            sys.stdout.write(RESET)
            break

def conta_itens(driver):
    games = driver.find_elements_by_css_selector('game-tile')
    return len(games)