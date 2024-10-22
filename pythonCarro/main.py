from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
import pandas as pd
import datetime
import pymysql.connections
from telas import *
from botoes import *
from bannerabastecimento import *
import requests
import os
import re
from functools import partial
from conexaosql import ConexaoSql
from loginsenha import LoginSenha
from pathlib import Path
from datetime import date
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from autocompletetextInput import AutocompleteTextInput



GUI = Builder.load_file("main.kv")

class MainApp(App):

    def build(self):
        self.loginsenha = LoginSenha()
        return GUI


    def on_start(self):
        arquivo = Path("logintoken.txt")
        # Verifica se o arquivo existe
        if arquivo.is_file():
            with open("logintoken.txt", "r") as arquivo:
                email = arquivo.read()
                senha = ""
            #print(email)
            self.carregar_dados_usuario(email, senha)
            self.mudar_tela("homepage")
            #print(f"O arquivo '{arquivo}' existe.")
        else:
            #print(f"O arquivo '{arquivo}' não foi encontrado.")
            pass

        arquivos = os.listdir("icones/fotos_perfil")
        page_fotoperfil = self.root.ids["mudarfotopage"]
        lista_fotos = page_fotoperfil.ids["lista_foto_perfil"]
        for foto in arquivos:
            imagem =ImageButton(source=f"icones/fotos_perfil/{foto}", on_release=partial(self.mudar_foto_perfil,foto))
            lista_fotos.add_widget(imagem)

    def carregar_dados_usuario(self, email, senha):
        id_usuario = email
        id_senha = senha
########################################################################################################
        # Buscar placas do banco de dados
        placas = self.buscar_placas(email)
        #print(placas)
        # Acessar o Spinner definido no .kv e preencher os valores
        meu_aplicativo = App.get_running_app()
        id_placa = meu_aplicativo.root.ids["cadastrarabastecimentopage"]
        id_placa.ids.id_placa.values = placas
#######################################################################################################

#######################################################################################################
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()
        if conn and cursor:

            cursor.execute("SELECT * FROM sd_usuarios WHERE email = %s LIMIT 1", (id_usuario,))
            resultado = cursor.fetchall()
            descricao = cursor.description
            #conexao_db.fechar_conexao(conn, cursor)
            avatar = pd.DataFrame(resultado)
            #print(avatar)
            foto_usuario = self.root.ids["foto_usuario"]
            foto_usuario.source = f"icones/fotos_perfil/{avatar[9][0]}"
            meu_aplicativo = App.get_running_app()
            id_usuarios = meu_aplicativo.root.ids["configpage"]
            id_usuarios.ids["id_usuario"].text = f"Seu email: {email}"
            id_usuarios.ids["id_usuario"].color = (0, 1, 0, 1)

            cursor.execute("SELECT * FROM sd_consumocarro WHERE email = %s order by placa,data desc", (id_usuario,))

            resultado = cursor.fetchall()
            descricao = cursor.description
            abastecimentos = pd.DataFrame(resultado)


            #print(abastecimentos)
            colunas = ['id', 'placa', 'km_total', 'km_rodado', 'custo_litro', 'custo_total', 'data', 'condutor', 'consumo',
                       'tipo', 'volume','logo_marca','email']
            abastecimentos = pd.DataFrame(resultado,columns=colunas)
            abastecimentos['data'] = abastecimentos['data'].apply(lambda x: x.strftime('%d/%m/%Y'))
            #abastecimentos['custo_litro'] = round(abastecimentos['custo_litro'], 2)
            # Usando round diretamente no DataFrame (sem precisar de float, Pandas já cuida disso)
            abastecimentos['custo_litro'] = abastecimentos['custo_litro'].astype(float).round(2)
            abastecimentos['km_total'] = abastecimentos['km_total'].astype(float).round(2)
            abastecimentos['km_rodado'] =abastecimentos['km_rodado'].astype(float).round(2)
            abastecimentos['custo_total']=abastecimentos['custo_total'].astype(float).round(2)
            abastecimentos['consumo'] = abastecimentos['consumo'].astype(float).round(2)
            # Índice correspondente ao campo "custo_total" e "data" na tupla
            indice_custo_total = 5
            indice_data = 6
            # Mês e ano que queremos filtrar (por exemplo, outubro de 2023)
            mes_especifico = float(date.today().strftime('%m'))
            ano_especifico = float(date.today().strftime('%Y'))

            def filtrar_por_mes(linha):
                #data = datetime.strptime(linha[indice_data], '%Y-%m-%d')  # converter string para objeto datetime
                data = linha[indice_data]
                return data.month == mes_especifico and data.year == ano_especifico


            # Filtrando registros pelo mês/ano específico e somando os custos totais
            total_custo = sum(
                float(linha[indice_custo_total]) for linha in resultado if filtrar_por_mes(linha)
            )

            # Exibir o total
            #print(f"Total do custo_total para {mes_especifico}/{ano_especifico}: {total_custo}")

            dic_abastecimentos = abastecimentos.to_dict(orient='records')

            #print(dic_abastecimentos)
            id_total_gasto = self.root.ids["homepage"]
            id_total_gasto.ids["id_total_gasto"].text = f"Total gasto do mês: R$ {round(total_custo, 2)}"

            try:
                pagina_homepage = self.root.ids["homepage"]
                lista_abastecimentos = pagina_homepage.ids["lista_abastecimento"]
                for abastecimento in dic_abastecimentos:
                    banner  = BannerAbastecimento(data = abastecimento['data'],
                                                  placa = abastecimento['placa'],
                                                  km_total = abastecimento['km_total'],
                                                  km_rodado = abastecimento['km_rodado'],
                                                  custo_litro = abastecimento['custo_litro'],
                                                  custo_total = abastecimento['custo_total'],
                                                  condutor = abastecimento['condutor'],
                                                  consumo = abastecimento['consumo'],
                                                  tipo = abastecimento['tipo'],
                                                  volume = abastecimento['volume'],
                                                  logo_marca = abastecimento['logo_marca'],
                                                  email = abastecimento['email'])
                    lista_abastecimentos.add_widget(banner)
            except:
                pass

    def gravar_carro(self,id_marca,id_modelo,id_versao,id_motor,id_placa,id_km_total,id_condutor):
        arquivo = Path("logintoken.txt")
        # Verifica se o arquivo existe
        if arquivo.is_file():
            with open("logintoken.txt", "r") as arquivo:
                email = arquivo.read()
                senha = ""
        meu_aplicativo = App.get_running_app()
        id_carro = meu_aplicativo.root.ids["cadastrarveiculopage"]
        id_marca =id_carro.ids["id_marca"].text
        id_modelo =id_carro.ids["id_modelo"].text
        id_versao =id_carro.ids["id_versao"].text
        id_motor  =id_carro.ids["id_motor"].text
        id_placa  =id_carro.ids["id_placa"].text
        id_km_total =id_carro.ids["id_km_total"].text
        id_condutor =id_carro.ids["id_condutor"].text
        id_bateria = "ND"
        id_autonomia ="ND"
        id_referencia ="ND"
        id_km_total = str(id_km_total)
        #print(type(id_placa), type(id_km_total), type(id_marca), type(id_modelo), type(id_versao), type(id_motor),
        #      type(id_bateria), type(id_autonomia), type(id_referencia), type(id_condutor), type(email))

        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()

        cursor.execute("SELECT placa FROM sd_cadastrocarro WHERE email=%s AND placa=%s", (email, id_placa))
        rows = cursor.fetchall()

        # Verificar se a consulta não retornou nenhuma linha (nenhum resultado)
        if not rows:
            # Se não houver resultados, você pode fazer o INSERT aqui
            try:
                cursor.execute("""
                    INSERT INTO `sd_cadastrocarro` 
                    (`placa`, `km_total`, `marca`, `modelo`, `versao`, `motor`, `bateria`, `autonomia`, `referencia`, `proprietario`, `email`) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                               (id_placa, id_km_total, id_marca, id_modelo, id_versao, id_motor, id_bateria,
                                id_autonomia, id_referencia, id_condutor, email)
                               )
                conn.commit()
                # Limpar variáveis após o insert
                id_marca = ""
                id_modelo = ""
                id_versao = ""
                id_motor = ""
                id_placa = ""
                id_km_total = ""
                id_condutor = ""
                id_bateria = "ND"
                id_autonomia = "ND"
                id_referencia = "ND"

                # Limpar os campos do formulário
                id_carro.ids["id_marca"].text = ""
                id_carro.ids["id_modelo"].text = ""
                id_carro.ids["id_versao"].text = ""
                id_carro.ids["id_motor"].text = ""
                id_carro.ids["id_placa"].text = ""
                id_carro.ids["id_km_total"].text = ""
                id_carro.ids["id_condutor"].text = ""
                self.mudar_tela("homepage")
            except Exception as e:
                print(id_placa, id_km_total, id_marca, id_modelo, id_versao, id_motor, id_bateria, id_autonomia,
                      id_referencia, id_condutor, email)

                print(f"Erro ao inserir os dados: {e}")

            #cursor.execute("INSERT INTO `sd_cadastrocarro`(`placa`, `km_total`, `marca`, `modelo`, `motor`, `bateria`, `autonomia`, `referencia`, `proprietario`, `email`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id_placa,id_km_total,id_marca,id_modelo,id_versao,id_motor,id_bateria,id_autonomia,id_referencia,id_condutor,email))
            #conn.commit()  # Não se esqueça de fazer commit após o insert
        else:
            print("Registro já existente.")

    def mudar_tela(self, id_tela):
        gerente_tela = self.root.ids["screen_manager"]
        gerente_tela.current = id_tela

    def mudar_foto_perfil(self, foto, email, *args):
        with open("logintoken.txt", "r") as arquivo:
            email = arquivo.read()
        foto_usuario = self.root.ids["foto_usuario"]
        foto_usuario.source = f"icones/fotos_perfil/{foto}"
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()
        cursor.execute("UPDATE `sd_usuarios` SET `foto`= %s WHERE email = %s", (foto, email))
        conn.commit()
        self.mudar_tela("configpage")

    def buscar_placas(self, email):
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()
        # Consulta para buscar as placas do condutor
        cursor.execute("SELECT placa FROM sd_cadastrocarro WHERE email=%s", (email,))
        rows = cursor.fetchall()

        # Retornar uma lista de placas
        return [row[0] for row in rows]

    def on_text(self, instance, value):
        # Limpar o dropdown
        self.dropdown.clear_widgets()
        # Buscar sugestões com base no texto digitado
        suggestions = buscar_sugestoes_modelo(value)
        for suggestion in suggestions:
            btn = Button(text=suggestion, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_suggestion(btn.text))
            self.dropdown.add_widget(btn)
        # Abrir o dropdown
        if suggestions:
            self.dropdown.open(self)

    def select_suggestion(self, text):
        self.text = text
        self.dropdown.dismiss()

    def calcula_consumo(self,id_placa,id_km_carro,id_km_rodado, id_total_custo, id_litros, id_tipo_comb):
        with open("logintoken.txt", "r") as arquivo:
            email = arquivo.read()
        data_atual = date.today()
        meu_aplicativo = App.get_running_app()
        id_carro = meu_aplicativo.root.ids["cadastrarabastecimentopage"]
        id_placa = id_carro.ids["id_placa"].text
        id_km_carro = id_carro.ids["id_km_carro"].text
        id_km_rodado = id_carro.ids["id_km_rodado"].text
        id_total_custo = id_carro.ids["id_total_custo"].text
        id_litros = id_carro.ids["id_litros"].text
        id_tipo_comb = id_carro.ids["id_tipo_comb"].text
        #print(id_placa,id_km_carro,id_km_rodado,id_total_custo,id_litros,id_tipo_comb)
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()
        try:
            # Consulta para buscar as placas do condutor

            cursor.execute("SELECT  km_total,proprietario,marca FROM sd_cadastrocarro WHERE placa=%s", (id_placa,))
            rows = cursor.fetchall()

            if rows:
                colunas = ['km_total', 'condutor', 'marca']
                km_carro = pd.DataFrame(rows, columns=colunas)

                # Acesse os valores diretamente da primeira linha
                km_carro_value = km_carro.iloc[0]["km_total"]
                condutor = km_carro.iloc[0]["condutor"]
                marca = km_carro.iloc[0]["marca"]
                logo_marca = marca.lower() + '.png'
                print(km_carro_value, condutor, marca, logo_marca)
            else:
                print("Nenhum dado encontrado para a placa fornecida.")


            id_km_carro = id_km_carro.replace(',', '')
            km_carro_value = str(km_carro_value).replace(',', '')
        finally:
        # Fechar cursor e conexão
            if cursor:
               cursor.close()
            if conn:
               conn.close()

        if not id_km_rodado and not id_km_carro:
            id_carro.ids["id_label"].text = "Km é obrigatorio!"
            id_carro.ids["id_label"].color = (1, 0, 0, 1)
        else:
            if not id_km_rodado:
                id_km_rodado = float(id_km_carro) - float(km_carro_value)
            else:
                id_km_carro = float(id_km_rodado) + float(km_carro_value)
            consumo =  float(id_km_rodado) / float(id_litros)
            consumo = f"{consumo:,.2f}"
            valor_custo = id_total_custo.replace("R$", "").strip()

            porlitro = float(valor_custo) / float(id_litros)
            porlitro = f"{porlitro:,.2f}"

            id_carro.ids["id_label"].text = f"Consumo calculado: {consumo} km/l"
            id_carro.ids["id_label"].color = (0, 1, 0, 1)
            print("Valor do Litro: ",porlitro)
            print(km_carro_value)
            print(id_km_carro)
            print(id_km_rodado)
            print(data_atual)
            print(condutor)
            print(logo_marca)
            ###############################################################################################
            conexao_db = ConexaoSql()
            conn, cursor = conexao_db.conexao()
            try:
                #UPDATE `sd_cadastrocarro` SET `km_total`='[value-3]' WHERE 1
                cursor.execute("UPDATE `sd_cadastrocarro` SET `km_total`= %s WHERE placa = %s", (str(id_km_carro),id_placa))
                conn.commit()
            finally:
                # Fechar cursor e conexão
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
       ##################################################################################################
#INSERT INTO `sd_consumocarro`(`id`, `placa`, `km_total`, `km_rodado`, `custo_litro`, `custo_total`, `data`, `condutor`, `po`, `tipo`, `volume`, `logo_marca`, `email`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]','[value-8]','[value-9]','[value-10]','[value-11]','[value-12]','[value-13]')
            conexao_db = ConexaoSql()
            conn, cursor = conexao_db.conexao()
            try:
                #UPDATE `sd_cadastrocarro` SET `km_total`='[value-3]' WHERE 1
                cursor.execute("INSERT INTO `sd_consumocarro`(`placa`, `km_total`, `km_rodado`, `custo_litro`, `custo_total`, `data`, `condutor`, `consumo`, `tipo`, `volume`, `logo_marca`, `email`) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               (id_placa,str(id_km_carro),str(id_km_rodado),str(porlitro),str(valor_custo),data_atual,condutor,str(consumo),id_tipo_comb,str(id_litros),logo_marca,email))
                conn.commit()
            finally:
                # Fechar cursor e conexão
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

###########################################################################################################
    def formatar_custo(self, instance):
        texto = instance.text

        # Remove qualquer caractere que não seja número ou ponto
        texto = ''.join([c for c in texto if c.isdigit() or c == '.'])

        if texto:
            # Formata o número como moeda
            try:
                valor = float(texto)
                texto_formatado = f"R$ {valor:,.2f}"
            except ValueError:
                texto_formatado = texto
        else:
            texto_formatado = ""

        # Atualiza o texto formatado no TextInput
        instance.text = texto_formatado

    def formatar_numero(self, instance):
        texto = instance.text

        # Remove qualquer caractere que não seja número ou ponto
        texto = ''.join([c for c in texto if c.isdigit() or c == '.'])

        if texto:
            # Formata o número como moeda
            try:
                valor = float(texto)
                texto_formatado = f"{valor:,.1f}"
            except ValueError:
                texto_formatado = texto
        else:
            texto_formatado = ""

        # Atualiza o texto formatado no TextInput
        instance.text = texto_formatado

MainApp().run()