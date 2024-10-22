import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from conexaosql import ConexaoSql
from pathlib import Path
import requests
import pandas as pd
import datetime
import pymysql.connections
import bcrypt
import re




# Função para buscar placas do banco de dados (substitua pelo seu banco)
def buscar_placas(email):
    conexao_db = ConexaoSql()
    conn, cursor = conexao_db.conexao()
    # Consulta para buscar as placas do condutor
    cursor.execute("SELECT placa FROM sd_cadastrocarro WHERE email=%s", (email,))
    rows = cursor.fetchall()

    # Retornar uma lista de placas
    return [row[0] for row in rows]


class MyLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__()

    arquivo = Path("logintoken.txt")
    if arquivo.is_file():
        with open("logintoken.txt", "r") as arquivo:
            email = arquivo.read()

        # Buscar placas do banco de dados
    placas = buscar_placas(email)
    #print(placas)
    # Acessar o Spinner definido no .kv e preencher os valores
    id_placa = App.get_running_app()
    id_placa = id_placa.root.get_screen('cadastrarabastecimentopage').ids.id_placa
    id_placa.ids.id_placa.values = placas
