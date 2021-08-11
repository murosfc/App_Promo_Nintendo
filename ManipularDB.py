import mysql.connector

#cria conexão com o banco de dados
def iniciar_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="abricó",
        database="db_apppromonintendo"
    )
    return mydb

#limpa as promos antigas
def limpa_db_antiga(tipo_extracao):
    DBapp = iniciar_db()
    meucursor = DBapp.cursor()
    if tipo_extracao == 1: #atualização de promo apenas
        meucursor.execute("DROP table jogos_em_promo")  # limpa a base antiga de promoções
        meucursor.execute(
            'CREATE TABLE Jogos_em_promo (DB_Nintendo_BR_nsuid VARCHAR(15) NOT NULL, sale_price FLOAT, validade_promo TEXT, FOREIGN KEY (DB_Nintendo_BR_nsuid) REFERENCES DB_Nintendo_BR(nsuid))')
        DBapp.commit()

#grava dados lidos no banco de dados
def gravar_db (dados_jogo_lido, tipo_extracao):
    DBapp = iniciar_db()
    meucursor = DBapp.cursor()
    if tipo_extracao == 1: #grava promos
            #grava na DB principal os que não foram gravados pelo limite de 1000 jogos do site inicial
            comando = (
                "INSERT IGNORE INTO db_nintendo_br VALUES (%s,%s,%s,%s)")  # atualiza os já existentes somente insere os novos
            valores = (dados_jogo_lido.nsuid, dados_jogo_lido.titulo, dados_jogo_lido.msrp, dados_jogo_lido.url_img)
            meucursor.execute(comando, valores)
            #fim do trecho anterior
            comando = ("INSERT INTO Jogos_em_promo VALUES (%s,%s,%s)")
            valores = (dados_jogo_lido.nsuid, dados_jogo_lido.sale_price, dados_jogo_lido.validade_promo)
            meucursor.execute(comando, valores)
            DBapp.commit()
    else: #grava todos os jogos
        comando = ("INSERT IGNORE INTO db_nintendo_br VALUES (%s,%s,%s,%s)") #atualiza os já existentes somente insere os novos
        valores = (dados_jogo_lido.nsuid,dados_jogo_lido.titulo,dados_jogo_lido.msrp,dados_jogo_lido.url_img)
        meucursor.execute (comando, valores)
        DBapp.commit()

def contar_jogos():
    DBapp = iniciar_db()
    meucursor = DBapp.cursor()
    meucursor.execute("SELECT COUNT(nsuid) FROM db_nintendo_br")
    (total,) = meucursor.fetchone()
    return int(total)
