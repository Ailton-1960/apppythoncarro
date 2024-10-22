from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

class BannerAbastecimento(GridLayout):

    def __init__(self, **kwargs):
        self.rows = 1
        super().__init__()

        with self.canvas:
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.atualizar_rec, size=self.atualizar_rec)

        data = kwargs["data"]
        placa = kwargs["placa"]
        km_total = kwargs["km_total"]
        km_rodado = kwargs["km_rodado"]
        consumo = kwargs["consumo"]
        logo_marca = kwargs["logo_marca"]
        custo_litro = kwargs["custo_litro"]
        custo_total = kwargs["custo_total"]

        esquerda = FloatLayout()
        esquerda_imagem = Image(pos_hint={"right": 1, "top": 0.99}, size_hint=(1, 0.75),
                            source=f"icones/logo_marca/{logo_marca}")
        esquerda_label = Label(text=placa, size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2})
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label)

        meio = FloatLayout()
        meio_label_data = Label(text=f"Data: {data}", size_hint=(1, 0.33),
                                       pos_hint={"right": 1, "top": 0.95})
        meio_label_custo_litro = Label(text=f"Litro:R$ {custo_litro}", size_hint=(1, 0.33),
                                        pos_hint={"right": 1, "top": 0.65})
        meio_label_custo_total = Label(text=f"Custo:R$ {custo_total}", size_hint=(1, 0.33),
                                      pos_hint={"right": 1, "top": 0.35})
        meio.add_widget(meio_label_data)
        meio.add_widget(meio_label_custo_litro)
        meio.add_widget(meio_label_custo_total)

        #meio_label = Label(text=data, size_hint=(1, 0.2), pos_hint={"right": 1, "top": 0.2})
        #meio.add_widget(meio_label)



        direita = FloatLayout()
        #direita_label_km_total = Label(text=f"Total: {km_total}", size_hint=(1, 0.33), pos_hint={"right": 1, "top":0.9})
        direita_label_km_rodado = Label(text=f"Km: {km_rodado}", size_hint=(1, 0.33), pos_hint={"right": 1, "top":0.80})
        direita_label_consumo = Label(text=f"Km/L: {consumo}", size_hint=(1, 0.33), pos_hint={"right": 1, "top":0.35})
        #direita.add_widget(direita_label_km_total)
        direita.add_widget(direita_label_km_rodado)
        direita.add_widget(direita_label_consumo)
        self.add_widget(esquerda)
        self.add_widget(meio)
        self.add_widget(direita)

    def atualizar_rec(self, *args):
        self.rec.pos = self.pos
        self.rec.size = self.size

