import pygame
import sys

from lopta import  *
from igrac import *
from threading import Timer

class Igra:
    def __init__(self, nivo = 1):
        self.nivo = nivo
        self.dva_igraca = False
        self.lopte = []
        self.igraci = [Igrac()]  #igrac class
        self.zavrsena_igra = False
        self.predjen_nivo = False
        self.restartuj_nivo = False
        self.izgubljeni_zivoti = False
        self.pokrenuto = True
        self.preostalo_vreme = 0


    def ucitaj_nivo(self, nivo):
        self.restartuj_nivo = True
        self.lopte = []
        self.izgubljeni_zivoti = False  #dead_player
        #if self.dva_igraca and len(self.igraci) == 1:
        #self.igraci.append(Igrac("igrac1.png"))    #igrac class
        for index, igrac in enumerate(self.igraci):
            index_igraca = index + 1
            broj_igraca = len(self.igraci)
            igrac.pocetna_pozicija(
                (640 / (broj_igraca + 1)) * index_igraca
            )
            igrac.ziv = True
        self.nivo = nivo
        self.predjen_nivo = False
        x = 200
        y = 250
        velicina = 2
        brzina = [1, 0]
        self.preostalo_vreme = 20
        self.lopte.append(Lopta(x, y, velicina, brzina))
        self._start_timer()

    def _start_timer(self):
        self._timer(1, self._tick_second, self.preostalo_vreme)

    def restart(self):
        self.ucitaj_nivo(self.nivo)

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
        for igrac in self.igraci:
            igrac.azuriraj()
        if not self.lopte:
            self.predjen_nivo = True


    def _timer(self, interval, worker_func, iterations=0):
        if iterations and not self.izgubljeni_zivoti and not \
                self.predjen_nivo and not self.restartuj_nivo:
            Timer(

                interval, self._timer,
                [interval, worker_func, 0 if iterations ==
                    0 else iterations - 1]
            ).start()
            worker_func()

    def _tick_second(self):
        self.preostalo_vreme -= 1
        #if self.preostalo_vreme == 0:
            #for igrac in self.igraci:
                #self._decrease_lives(igrac)