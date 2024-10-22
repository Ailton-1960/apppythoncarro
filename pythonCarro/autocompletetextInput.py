from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.app import App
from conexaosql import ConexaoSql

class AutocompleteTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.dropdown = DropDown()  # Inicializa o DropDown aqui

    def on_text(self, instance, value):
        # Recriar o DropDown a cada vez que o texto for alterado
        dropdown = DropDown()

        # Verifica se estamos buscando marcas ou modelos
        if self.tipo == "marca":
            suggestions = self.buscar_marcas(value)
        elif self.tipo == "modelo":
            suggestions = self.buscar_modelos(value)
        elif self.tipo == "versao":
            suggestions = self.buscar_versao(value)

        #   print(suggestions)
        # Adicionar as sugestões ao dropdown
        for suggestion in suggestions:
            btn = Button(text=suggestion, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_suggestion(btn.text, dropdown))
            dropdown.add_widget(btn)

        # Mostrar o dropdown se houver sugestões
        if suggestions:
            dropdown.open(instance)

    def select_suggestion(self, text, dropdown):
        if dropdown:
            dropdown.dismiss()
        # Preencher o campo de texto com a sugestão selecionada
        self.text = text

        if self.tipo == "versao":
            self.busca_motor()

        if self.tipo == "marca":
            meu_aplicativo = App.get_running_app()
            modelos_input = meu_aplicativo.root.ids["cadastrarveiculopage"].ids["id_modelo"]
            modelos_input.on_text(self, "")

    def buscar_marcas(self, query):
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()

        # Consulta para buscar as marcas do banco de dados
        cursor.execute("SELECT marcas FROM sd_marcas ORDER BY marcas")
        resultados = cursor.fetchall()  # Isso retorna uma lista de tuplas, ex: [('Toyota',), ('Honda',), ...]

        # Extrair apenas as marcas (strings) das tuplas
        marcas = [resultado[0] for resultado in resultados]  # Cria uma lista só com as strings das marcas

        # Filtrar as marcas com base no texto digitado (query)
        return [marca for marca in marcas if marca.lower().startswith(query.lower())]

    def buscar_modelos(self, query):
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()

        meu_aplicativo = App.get_running_app()
        id_marcas = meu_aplicativo.root.ids["cadastrarveiculopage"]
        marca = id_marcas.ids["id_marca"].text
        # Consulta para buscar as marcas do banco de dados
        cursor.execute("SELECT modelo FROM sd_modelos WHERE marca = %s ORDER BY modelo", (marca,))
        resultados = cursor.fetchall()

        # Extrair apenas as marcas (strings) das tuplas
        modelos = [resultado[0] for resultado in resultados]  # Cria uma lista só com as strings das modelos

        # Filtrar as marcas com base no texto digitado (query)
        #return [marca for marca in marcas if marca.lower().startswith(query.lower())]
        return [modelo for modelo in modelos if query.lower() in modelo.lower()]
    def buscar_versao(self, query):
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()

        meu_aplicativo = App.get_running_app()
        id_carros = meu_aplicativo.root.ids["cadastrarveiculopage"]
        marca = id_carros.ids["id_marca"].text
        modelo = id_carros.ids["id_modelo"].text
        # Consulta para buscar as marcas do banco de dados
        cursor.execute("SELECT versao,motor FROM sd_modelos WHERE marca = %s AND modelo = %s ORDER BY modelo", (marca,modelo,))
        resultados = cursor.fetchall()

        # Extrair apenas as marcas (strings) das tuplas
        versaos = [resultado[0] for resultado in resultados]  # Cria uma lista só com as strings das modelos

        # Filtrar as marcas com base no texto digitado (query)
        #return [marca for marca in marcas if marca.lower().startswith(query.lower())]
        return [versao for versao in versaos if query.lower() in versao.lower()]

    def busca_motor(self):
        # Método para preencher o campo motor após selecionar a versão
        conexao_db = ConexaoSql()
        conn, cursor = conexao_db.conexao()

        meu_aplicativo = App.get_running_app()
        id_versao = meu_aplicativo.root.ids["cadastrarveiculopage"]
        versao = id_versao.ids["id_versao"].text

        # Busca o motor baseado na versão selecionada
        cursor.execute("SELECT motor FROM sd_modelos WHERE versao = %s", (versao,))
        resultado = cursor.fetchone()

        if resultado:
            # Preenche o campo de texto do motor
            id_motor = meu_aplicativo.root.ids["cadastrarveiculopage"].ids["id_motor"]
            id_motor.text = resultado[0]  # Define