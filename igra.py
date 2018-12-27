import pygame
import sys

from lopta import  *
from igrac import *

class Igra:
    def __init__(self, nivo = 1):
        self.nivo = nivo
        self.dva_igraca = False
        self.lopte = []
        self.igraci = []  #igrac class
        self.skokovi = [] #sin(ax)
        self.zavrsena_igra = False
        self.predjen_nivo = False
        self.restartuj_nivo = False
        self.izgubljeni_zivoti = False
        self.pokrenuto = True

    def restart(self):
        self.ucitaj_nivo(self.nivo)

    def ucitaj_nivo(self, nivo):
        self.restartuj_nivo = True
        self.lopte = []
        self.skokovi = []
        self.izgubljeni_zivoti = False  #dead_player
        self.nivo = nivo
        self.predjen_nivo = False
        if self.dva_igraca and len(self.igraci) == 1:
            self.igraci.append()    #igrac class
        for index, igrac in enumerate(self.igraci):
            index_igraca = index + 1
            broj_igraca = len(self.igraci)
            #pozicija
            #ucitavnje levela
            x = 200
            y = 250
            velicina = 2
            brzina = [3, 0]
            self.lopte.append(Lopta(x, y, velicina, brzina))
    def azuriraj(self):
        if self.predjen_nivo:
            self.ucitaj_nivo(self.nivo + 1)
        if self.zavrsena_igra:
            self.pokrenuto = False
            pygame.quit()
            sys.exit()
        if self.izgubljeni_zivoti:
            self.restart()
        #kolizija         self._check_for_collisions()
        for lopta in self.lopte:
            lopta.azuriraj()
        if not self.lopte:
            self.predjen_nivo = True
