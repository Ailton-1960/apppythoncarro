import pandas as pd
import datetime
import pymysql.connections


class ConexaoSql():

    def conexao(self):
        config = {
            'user': 'sidef2',
            'password': 'SD@sidef1804',
            'host': 'mysql.sidef.com.br',  # Remova o 'mysql:host='
            'database': 'sidef2'
        }

        try:
            conn = pymysql.connect(**config)
            cursor = conn.cursor()
            return conn, cursor

        except pymysql.MySQLError as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None, None

    def fechar_conexao(self, conn, cursor):
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Conexão fechada com sucesso!")
