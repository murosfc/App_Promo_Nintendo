-- SCRIPT COM COMANDOS DDL PARA 
-- CRIACAO E ATIVAÇÃO DO DATABASE DO APP DE PROMOS NINTENDO
-- AUTOR: FELIPE CELESTINO MUROS
-- VER. 1.0 21/05/2021


create database db_appPromoNintendo;
use db_appPromoNintendo;

CREATE TABLE DB_Nintendo_BR (
  nsuid VARCHAR(15) NOT NULL,
  titulo TEXT,
  msrp FLOAT,
  img_url TEXT,
  PRIMARY KEY(nsuid)
);

CREATE TABLE Jogos_em_promo (
  DB_Nintendo_BR_nsuid VARCHAR(15) NOT NULL,
  sale_price FLOAT,
  validade_promo TEXT,
  FOREIGN KEY (DB_Nintendo_BR_nsuid) REFERENCES DB_Nintendo_BR(nsuid)
);

