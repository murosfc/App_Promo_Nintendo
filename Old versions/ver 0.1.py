'''
Ver. 0.1 Criação do Scrapping em 20/05/2021
Ver. 0.2 Adicionado a extração do nsuid (identificador único do título) 21/05/2021
'''
from selenium import webdriver
import pandas as pd
import os
import time

Ver = "0.1"

class dados_dos_jogos:
    def __init__(self):
        self.nsuid = ''
        self.titulo = ''
        self.msrp = '' # msrp = Manufacturer's Suggested Retail Price
        self.sale_price = ''
        self.validade_promo = ''
        self.url_img = ''
    pass

def iniciar_navegador(tipo_extracao):
    if tipo_extracao == 1:
        link = "https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q=&dFR[generalFilters][0]=Deals"
    else:
        link = 'https://www.nintendo.com/pt_BR/games/game-guide/#filter/:q='
    driver = webdriver.Chrome()
    driver.get(link)
    driver.minimize_window()
    return driver

#iniciar o dataframe organizando as colunas
def iniciar_dataframe():
    tabela= pd.DataFrame(columns= ['NSUID', 'Título do jogo', 'Preço Normal', 'Preço com desconto', 'Validade da promoção', 'URL imagem'])
    return tabela

# salva o jogo lido no banco de dados
def df_insert(tabela, dados):
    #print(dados.titulo + ". Custava " + dados.msrp + ". Até dia " + dados.validade_promo + " custará " + dados.sale_price)
    nova_linha = {'NSUID': dados.nsuid, 'Título do jogo': dados.titulo, 'Preço Normal': dados.msrp, 'Preço com desconto': dados.sale_price,
                  'Validade da promoção': dados.validade_promo, 'URL imagem': dados.url_img}
    tabela = tabela.append(nova_linha, ignore_index=True)
    return tabela

# exporta dataframe para um arquivo em excel
def exportar_df(tabela_dados):
    print('Leitura concluída, gerando arquivos de saída')
    driver.quit()
    if tipo_extracao == 1:
        nome_arquivo = ('db_promo.xlsx')
    else:
        nome_arquivo = ('db_completa.xlsx')
    tabela_dados.to_excel(nome_arquivo)
    if os.path.exists(nome_arquivo):
        print('Tabela criada com sucesso')
    else:
        print('Erro ao criar arquivo de saída de dados')

def scraping_nintendo(tabela_dados, tipo_extracao):
    indice = 1
    dados_jogo_lido = dados_dos_jogos()
    while True:
        try:
            driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
        except Exception:
            exportar_df(tabela_dados)  # exporta o dataframe em uma planilha do excel
            return (
                        indice - 1)  # encerra o scrapping caso não encontre mais jogos e retorna a quantidade de jogos em promoção
        try:
            driver.find_element_by_id("btn-load-more").click()  # clica no botão para carregar mais
        except Exception:
            pass
        if tipo_extracao == 1
            dados_jogo_lido.nsuid = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('nsuid')
            dados_jogo_lido.sale_price = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('sale-price')
            dados_jogo_lido.validade_promo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('date')
            tabela_dados = df_insert(tabela_dados,
                                     dados_jogo_lido)  # chama a função para arquivar os dados lidos no dataframe
        else:
            dados_jogo_lido.nsuid = driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('nsuid')
            dados_jogo_lido.titulo = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile/h3').text
            dados_jogo_lido.msrp = driver.find_element_by_xpath(
                f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('msrp')
            dados_jogo_lido.url_img = driver.find_element_by_xpath(f'//*[@id="games-list-container"]/ul/li[{indice}]/game-tile').get_attribute('image')
            tabela_dados = df_insert(tabela_dados, dados_jogo_lido)  # chama a função para arquivar os dados lidos no dataframe
        indice += 1

# programa principal
inicio = time.time()
tipo_extracao = 0 #enviar 1 para promoções e 0 para todos os jogos
print('Iniciando a leitura do site da Nintendo Brasil')
driver = iniciar_navegador(tipo_extracao)
tabela_dados = iniciar_dataframe ()  # tabela que armazenará os dados dos jogos
quantidade_itens_promo = scraping_nintendo(tabela_dados)  # executa a leitura e gravação dos dados obtido no site da nintendo
print(f'quantidade de itens em promoção {quantidade_itens_promo}')
print('Programa finalizado')
print("Tempo gasto para processar", time.time() - inicio)

