-- SCRIPT COM COMANDOS DDL PARA 
-- CRIACAO E ATIVAÇÃO DO DATABASE DO APP DE PROMOS NINTENDO
-- AUTOR: FELIPE CELESTINO MUROS
-- VER. 1.0 21/05/2021


create database db_appPromoNintendo;
use db_appPromoNintendo;

CREATE TABLE DB_Nintendo_BR (
  nsuid VARCHAR(20) NOT NULL,
  titulo TEXT,
  msrp FLOAT,
  img_url TEXT,
  PRIMARY KEY(nsuid)
);

CREATE TABLE Jogos_em_promo (
  DB_Nintendo_BR_nsuid VARCHAR(20) NOT NULL,
  sale_price FLOAT,
  validade_promo TEXT,
  FOREIGN KEY (DB_Nintendo_BR_nsuid) REFERENCES DB_Nintendo_BR(nsuid)
);

create table users (   
    id VARCHAR (20) NOT NULL,
    pass VARCHAR (32) NOT NULL, 
    email VARCHAR (50),
    rec_key VARCHAR (5),
	PRIMARY KEY(id)    
  );
  
create table user_favs (
	FK_nsuid VARCHAR(20) NOT NULL,
	FK_user_id VARCHAR (20) NOT NULL,
    FOREIGN KEY (FK_nsuid) REFERENCES DB_Nintendo_BR(nsuid),
    FOREIGN KEY (FK_user_id) REFERENCES users(id)
    );

