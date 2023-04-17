from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.graphics import Line, Color

from random import choice
from pprint import pprint

class Touch(Widget):
    pass
        

class PionX(Image):
    light = NumericProperty(0)


class PionY(Image):
    light = NumericProperty(0)


class Game(Widget):
    demi = NumericProperty(200)
    vLine = ListProperty([-10,-10,-10,-10])
    tiroirX = []
    tiroirY = []
    tour = 'x'
    phase = 'placement'
    jeuxState = None
    pause = True

    def start(self):
        self.clean()
        self.tiroirX = [1,2,3]
        self.tiroirY = [1,2,3]
        self.tour = choice(['x','y'])
        self.phase = 'placement'
        self.jeuxState = None
        self.vLine = [-10,-10,-10,-10]
        self.pause = False
        print("_________________began_______________________")

    def phaseTransition(self):
        if len(self.tiroirX) == 0 and len(self.tiroirY) == 0:
            self.phase = 'jeux'
            print('transition fait')

    def on_touch_down(self, touch):
        if not self.pause:
            if self.phase == 'placement':
                self.placementPhase(touch)
            elif self.phase == 'jeux':
                self.jeuxPhase(touch)
        else:
            self.start()

    def tourner(self):
        if self.tour == 'y':
            self.tour = 'x'
        elif self.tour == 'x':
            self.tour = 'y'
        self.tourLight()

    def tourLight(self):
        for widget in self.children:
            if widget.type == "pion":
                if self.tour == widget.genre:
                    widget.light = .2
                else:
                    widget.light = 0


    def placementPhase(self, touch):
        for widget in self.children:
            if widget.collide_point(*touch.pos) and widget.type == 'touch' and widget.occupation == 'vide':
                if self.tour == 'x':
                    self.addPionX(widget.center, widget.num)
                elif self.tour == 'y':
                    self.addPionY(widget.center, widget.num)
                widget.occupation = 'pion'
                widget.light = 1
                self.verificationDeVictoire()
                break

    def jeuxPhase(self, touch):
        for widget in self.children:
            if widget.collide_point(*touch.pos):
                if widget.type == 'pion' and widget.genre == self.tour:
                    self.tourLight()
                    widget.light = .4
                    self.jeuxState = widget
                    print('charger')
                elif widget.type == 'touch' and self.jeuxState:
                    self.jeuxState.center = widget.center
                    self.jeuxState.posIndice = widget.num
                    self.jeuxState = None
                    self.tourner()
                    self.verificationDeVictoire()
                    print('decharger')
                elif not self.jeuxState:
                    print('rien')
                break
            
    def verificationDeVictoire(self):
        poinsX = []
        xxx = []
        poinsY = []
        yyy = []
        for widget in self.children:
            if widget.type == 'pion':
                if widget.genre == 'x':
                    poinsX.append(widget.posIndice)
                    xxx.append(widget.center)
                elif widget.genre == 'y':
                    poinsY.append(widget.posIndice)
                    yyy.append(widget.center)
        if self.poinAligner(poinsX):
            self.victoireLine(xxx)
        elif self.poinAligner(poinsY):
            self.victoireLine(yyy)
        else:
            print('pas de victoire')

    def victoireLine(self, poins):
        self.vLine = [*poins[0],*poins[1],*poins[2]]
        self.pause = True

    def clean(self):
        while len(self.children) > 9:
            for widget in self.children:
                if widget.type == 'pion':
                    self.remove_widget(widget)
                elif widget.type == 'touch':
                    widget.occupation = 'vide'

    def  poinAligner(self, poins):
        out = False
        if 1 in poins and 2 in poins and 3 in poins:
            out = poins
        elif 3 in poins and 4 in poins and 5 in poins:
            out = poins
        elif 5 in poins and 6 in poins and 7 in poins:
            out = poins
        elif 1 in poins and 7 in poins and 8 in poins:
            out = poins
        elif 2 in poins and 6 in poins and 9 in poins:
            out = poins
        elif 4 in poins and 8 in poins and 9 in poins:
            out = poins        
        elif 1 in poins and 5 in poins and 9 in poins:
            out = poins
        elif 3 in poins and 7 in poins and 9 in poins:
            out = poins
        else:
            out = False
        return out

    def takePion(self):
        pass

    def putPion(self):
        pass

    def addPionX(self, pos, posIndice):
        pion = PionX()
        pion.center = pos
        pion.posIndice = posIndice
        self.add_widget(pion)
        self.tourner()
        self.tiroirX.pop()
        self.phaseTransition()
    
    def addPionY(self, pos, posIndice):
        pion = PionY()
        pion.center = pos
        pion.posIndice = posIndice
        self.add_widget(pion)
        self.tourner()
        self.tiroirY.pop()
        self.phaseTransition()


class TicTacToeApp(App):
    def build(self):
        game = Game()
        game.start()
        return game

if __name__ == '__main__':
    TicTacToeApp().run()