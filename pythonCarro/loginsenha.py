import requests
import pandas as pd
import datetime
import pymysql.connections
import bcrypt
import re
from kivy.app import App
from conexaosql import ConexaoSql
from pathlib import Path


class LoginSenha():

    def criar_conta(self, email, senha):
        if self.validar_email(email):
            #print(f"O email '{email}' é válido.")
            # Exemplo de uso

            if self.validar_senha(senha):
                #print("A senha é válida.")
                with open("logintoken.txt", "w") as arquivo:
                    arquivo.write(email)

            conexao_db = ConexaoSql()
            conn, cursor = conexao_db.conexao()
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

            data_hora_atual = datetime.datetime.now()
        # Extrai a hora e a data separadamente, se necessário
            hora = data_hora_atual.strftime("%H:%M:%S")  # Hora no formato HH:MM:SS
            data = data_hora_atual.strftime("%Y-%m-%d")  # Data no formato YYYY-MM-DD

            if conn and cursor:
                cursor.execute("INSERT INTO `sd_usuarios`(`usuario`, `senha`, `email`, `nivel`, `setor`, `status`, `horas`, `data`, `foto`, `password`) "
                               "VALUES ('',%s,%s,'2','Carro','Ativo',%s,%s,'foto1.png','')", (hashed_senha.decode('utf-8'), email, hora, data))
                conn.commit()
                resultado = cursor.fetchone()



            else:
                return False
                #print("A senha é inválida.")
        else:
            return False
            #print(f"O email '{email}' é inválido.")





    def fazer_login(self, email, senha):

        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()
        if conn and cursor:
            cursor.execute("SELECT senha FROM sd_usuarios WHERE email = %s LIMIT 1", (email,))
            resultado = cursor.fetchone()
        # Consulta para buscar a senha hash no banco de dados

        if resultado:
            hashed_senha = resultado[0]  # A senha deve ser uma string armazenada como hash
            # Verificando a senha inserida pelo usuário com o hash armazenado
            if bcrypt.checkpw(senha.encode('utf-8'), hashed_senha.encode('utf-8')):
                meu_aplicativo = App.get_running_app()
                meu_aplicativo.carregar_dados_usuario(email, senha)
                arquivo = Path("logintoken.txt")
                with open("logintoken.txt", "w") as arquivo:
                    arquivo.write(email)

                meu_aplicativo.mudar_tela("homepage")
                # menssagem_erro = "Senha correta"
                # meu_aplicativo = App.get_running_app()
                # login_page = meu_aplicativo.root.ids["loginpage"]
                # login_page.ids["menssagem_login"].text = menssagem_erro
                # login_page.ids["menssagem_login"].color = (0, 1, 0, 1)
            else:
                menssagem_erro = "Senha incorreta"
                meu_aplicativo = App.get_running_app()
                login_page = meu_aplicativo.root.ids["loginpage"]
                login_page.ids["menssagem_login"].text = menssagem_erro
                login_page.ids["menssagem_login"].color = (1, 0, 0, 1)
        else:
            menssagem_erro = "Usuário não encontrado"
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = (0.9, 0, 0, 0.9)

    def validar_email(self, email):
        # Expressão regular para validar o formato de um email
        padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # Verifica se o email corresponde ao padrão
        if re.match(padrao_email, email):
            return True
        else:
            menssagem_erro = "O email é invalido."
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = ("#D61493")
            return False


    def validar_senha(self, senha):
            # Verifica se a senha tem pelo menos 8 caracteres
        if len(senha) < 8:
            menssagem_erro = "A senha deve ter no mínimo 8 caracteres."
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = ("#D61493")
            #print("A senha deve ter no mínimo 8 caracteres.")
            return False

            # Verifica se a senha contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', senha):
            menssagem_erro = "A senha deve conter pelo menos uma letra maiúscula."
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = ("#D61493")
            #print("A senha deve conter pelo menos uma letra maiúscula.")
            return False

            # Verifica se a senha contém pelo menos uma letra minúscula
        if not re.search(r'[a-z]', senha):
            menssagem_erro = "A senha deve conter pelo menos uma letra minúscula."
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = ("#D61493")
            #print("A senha deve conter pelo menos uma letra minúscula.")
            return False

            # Verifica se a senha contém pelo menos um número
        if not re.search(r'[0-9]', senha):
            menssagem_erro = "A senha deve conter pelo menos um número."
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = ("#D61493")
            #print("A senha deve conter pelo menos um número.")
            return False

            # Verifica se a senha contém pelo menos um símbolo especial
        if not re.search(r'[\W_]', senha):  # \W é qualquer caractere não alfanumérico
            menssagem_erro = "A senha deve conter pelo menos um símbolo especial."
            meu_aplicativo = App.get_running_app()
            login_page = meu_aplicativo.root.ids["loginpage"]
            login_page.ids["menssagem_login"].text = menssagem_erro
            login_page.ids["menssagem_login"].color = ("#D61493")
            #print("A senha deve conter pelo menos um símbolo especial.")
            return False

            # Se passou por todas as verificações
        return True



#######################################################################################################################
        # Recuperar todos os emails e senhas em texto simples (assumindo que estão armazenadas como texto simples)
        #cursor.execute("SELECT id, senha FROM sd_usuarios")
        #usuarios = cursor.fetchall()

        # Para cada usuário, gerar o hash da senha e atualizar o banco de dados
        #for usuario in usuarios:
        #    user_id = usuario[0]
        #    senha_texto = usuario[1]

            # Gerar o hash da senha
            #hashed_senha = bcrypt.hashpw(senha_texto.encode('utf-8'), bcrypt.gensalt())

            # Atualizar o banco de dados com a nova senha em hash
            #cursor.execute("UPDATE sd_usuarios SET senha = %s WHERE id = %s", (hashed_senha.decode('utf-8'), user_id))

        # Confirmar as atualizações no banco de dados
        #conn.commit()

        # Fechar a conexão
        #cursor.close()
        #conn.close()

        #print("Todas as senhas foram atualizadas com sucesso.")
################################################################################################################

        #resultado = cursor.fetchall()
        #colunas = ['id', 'usuario', 'senha', 'email', 'nivel', 'setor', 'status', 'horas', 'data', 'foto']

        #usuario = pd.DataFrame(resultado, columns=colunas)
        #usuario['data'] = usuario['data'].apply(lambda x: x.strftime('%d/%m/%Y'))
        #dic_usuario = usuario.to_dict(orient='records')
        #print(usuario)

        #foto_usuario = self.root.ids["foto_usuario"]
        #foto_usuario.source = f"icones/fotos_perfil/{avatar[9][0]}"
###################################################################################################################