'''
Change log:
Ver. 0.1 Criação do Scrapping em 20/05/2021
Ver. 1.0 Adicionado a extração do nsuid (identificador único do título) e interação com mysql 21/05/2021
Ver. 1.1 Mudanças na abordagem de limpar dados antigos da DB 22/05/2021 resumindo 3 funções em apenas 1
Ver. 1.2 Utilizando a atualização de DB, não mais o conceito de apagar e criar nova
Ver. 1.3 Abrindo os botões de mais antes de iniciar a leitura e contando a quantidade de itens
Ver. 1.4 Inverte a ordem alfabética para ler todos os jogos
Ver. 1.5 Divisão do programa em módulos
'''

Ver = "1.5"

#import bibliotecas
import time
import sys
#import dos módulos
import ManipularDB
import scrapper
import Ferramentas

############# PROGRAMA PRINCIPAL #################
#inicia cores
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

sys.stdout.write(BOLD + BLUE)
print (f"\nBem vindo ao programa de scrapping de jogos anunciados na eshop Nintedo BR\nFeito por Felipe Muros\nVersão atual {Ver}")
sys.stdout.write(RESET)
inicio = time.time()
tipo_extracao = 1 #insira 0 para forçar atualização completa
driver = Ferramentas.iniciar_navegador(0)
jogos_disponiveis=int(driver.find_element_by_id("result-count").text.replace(" resultados",""))
if (ManipularDB.contar_jogos() != jogos_disponiveis and tipo_extracao ==1):
    tipo_extracao=0

if (tipo_extracao == 1):
    driver.find_element_by_xpath('//label[@for="check-generalFilters-Deals"]').click()
    scrapper.scraping_nintendo(tipo_extracao, driver)
else:
    sys.stdout.write(CYAN)
    scrapper.scraping_nintendo(tipo_extracao, driver)
    print("Tempo gasto para leitura completa", "{:.2f}".format((time.time() - inicio) / 60), "minutos")
    sys.stdout.write(RESET)

sys.stdout.write(CYAN)
print('\n\nPrograma finalizado')
sys.stdout.write(RESET)
print("Tempo total gasto para processar", "{:.2f}".format((time.time() - inicio)/60), "minutos")
driver.quit()

