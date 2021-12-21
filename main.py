from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors.magic_behavior import MagicBehavior
from kivymd.uix.button.button import MDIconButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.fitimage import FitImage
from kivy.utils import get_color_from_hex as rgba

strButtons = ['C', '^', 'del', ' / ',
        '7', '8', '9', ' x ',
        '4', '5', '6', ' - ',
        '1', '2', '3', ' + ',
        '+/-','0', '.', '=']

class Visor(MDBoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(
            text='0',
            font_style='H5',
            font_name='Poppins',
            halign='right')
        self.label.color = rgba('#FFFFFF')
        self.add_widget(self.label)
        self.padding = 50, 50, 50, 50
        self.size_hint = 0.68, 0.5
        self.radius = 30, 30, 30, 30
        self.md_bg_color = rgba('#1038ea')
        self.opacity = 0.8
    
    def addText(self, str):
        if self.label.text == '0':
            self.label.text = str
            return
        self.label.text += str

    def rmText(self):
        self.label.text = self.label.text[:-1]

    def clearText(self):
        self.label.text = '0'

    def post_result(self):
        aux = self.label.text.replace('x', '*')
        aux = aux.replace('^', '**')
        try:
            resultado = eval(aux)
        except:
            self.setText('Error')
            return
        if isinstance(resultado, (float, int)):
            self.setText(str(round(resultado, 8)).removesuffix('.0'))

    def setText(self, str):
        self.label.text = str

    def getText(self) -> str:
        return self.label.text

class CalcButton(MDFillRoundFlatButton):
    def __init__(self, visor, **kwargs):
        super().__init__(**kwargs)
        self.text_color = rgba('#FFFFFF')
        self.visor = visor

    def on_release(self):
        botao = self.text
        if botao == '^':
            self.visor.setText('('+self.visor.getText()+')^')
            return
        if botao == 'del':
            if len(self.visor.getText()) == 1:
                self.visor.clearText()
            else:
                self.visor.rmText()
            return
        if botao == 'C':
            self.visor.clearText()
            return
        if botao == '=':
            self.visor.post_result()
            return
        self.visor.addText(str(botao))
        return

class TecladoCalculadora(MDGridLayout):
    def __init__(self, visor, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.adaptive_size = True
        self.spacing = 15
        self.padding = 10, 10, 10, 10
        for i in strButtons:
            self.add_widget(CalcButton(visor, text=i))

    def on_release(self):
        botao = self.text
        if botao == '^':
            self.visor.setText('('+self.visor.getText()+')^')
            return
        if botao == 'del':
            if len(self.visor.getText()) == 1:
                self.visor.clearText()
            else:
                self.visor.rmText()
            return
        if botao == 'C':
            self.visor.clearText()
            return
        if botao == '=':
            self.visor.post_result()
            return
        self.visor.addText(str(botao))
        return

class MagicButton(MDIconButton, MagicBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = 'circle-half-full'
        self.aux = 'Light'

    def on_release(self):
        self.twist()
        if self.aux == 'Light':
            Simple_Calculator().theme_cls.theme_style = 'Dark'
            self.aux = 'Dark'
        else:
            Simple_Calculator().theme_cls.theme_style = 'Light'
            self.aux = 'Light'
        return


class Home(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.orientation = 'vertical'
        self.visor = Visor()
        white_circle = MDBoxLayout()
        white_circle.adaptive_size = True
        white_circle.radius = 500, 500, 500, 500
        white_circle.md_bg_color = rgba('#FFFFFF')
        white_circle.opacity = 0.5
        themeB = MagicButton()
        white_circle.add_widget(themeB)
        ancs = [
            MDAnchorLayout(anchor_x='center', anchor_y='center'),
            MDAnchorLayout(anchor_x='center', anchor_y='center'),
            MDAnchorLayout(anchor_x='right', anchor_y='top')]
        ancs[2].add_widget(white_circle)
        ancs[0].add_widget(ancs[2])
        ancs[0].add_widget(self.visor)
        ancs[1].add_widget(TecladoCalculadora(self.visor))
        self.add_widget(ancs[0])
        self.add_widget(ancs[1])

class Simple_Calculator(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.homeScreen = MDScreen()
        img = FitImage(source='math_.png')
        img.opacity = 0.2
        self.homeScreen.add_widget(img)
        self.homeScreen.add_widget(Home())

    def build_app(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'DeepPurple'
        self.theme_cls.primary_hue = '700'
        self.icon = 'icon.png'
        return self.homeScreen

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

if __name__ == '__main__':
    reset()
    Simple_Calculator().run()