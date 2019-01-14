from oruzje import *
from konekcija_za_igru import *
from client import *


class Igrac(pygame.sprite.Sprite):
    def __init__(self, slika):
        self.slika = pygame.image.load(PUTANJA_SLIKE + slika)
        self.rect = self.slika.get_rect()
        self.desno = False
        self.levo = False
        self.oruzje = Oruzje()
        self.zivoti = 3
        self.pocetna_pozicija()
        self.ziv = True
        self.prvi_igrac = True

    def pucaj(self):
        self.oruzje = Oruzje(self.rect.centerx, self.rect.top)
        self.oruzje.ziv = True
    def azuriraj(self):
        if self.prvi_igrac:
            self.slika = pygame.image.load(PUTANJA_SLIKE + "igrac1.png")
        else:
            self.slika = pygame.image.load(PUTANJA_SLIKE + "igrac2.png")
        if self.levo and self.rect.left >= 33:
            if self.prvi_igrac:
                self.slika = pygame.image.load(PUTANJA_SLIKE + "igrac1LevoPNG.png")
            else:
                self.slika = pygame.image.load(PUTANJA_SLIKE + "igrac2LevoPNG.png")
            self.rect = self.rect.move(-5, 0)
        if self.desno and self.rect.right <= SIRINA - 39:
            if self.prvi_igrac:
                self.slika = pygame.image.load(PUTANJA_SLIKE + "igrac1DesnoPNG.png")
            else:
                self.slika = pygame.image.load(PUTANJA_SLIKE + "igrac2DesnoPNG.png")
            self.rect = self.rect.move(5, 0)
        if self.oruzje.ziv:
            self.oruzje.azuriraj()

    def pocetna_pozicija(self, x = SIRINA/2, y = VISINA):
        self.rect.centerx, self.rect.bottom = x, y
        self.oruzje.ziv = False

    def make_data_package(self):
        datax = str(self.rect.centerx).rjust(4, '0')
        datay = str(self.rect.centery).rjust(4, '0')

        if self.oruzje.ziv:
            dataorx = str(self.oruzje.rect.centerx).rjust(4,'0')
            dataory = str(self.oruzje.rect.centery).rjust(4,'0')
            return datax + datay + dataorx + dataory

        return datax + datay

def ip_value(ip):
    """ ip_value returns ip-string as integer """
    return int(''.join([x.rjust(3, '0') for x in ip.split('.')]))

def define_players(MY_SERVER_HOST, OTHER_HOST):
    if ip_value(MY_SERVER_HOST) > ip_value(OTHER_HOST):
        me = Igrac_1()
        enemy = Igrac_2()
        me_igrac1 = True
    else:
        me = Igrac_2()
        enemy = Igrac_1()
        me_igrac1 = False
    return me, enemy, me_igrac1

class Igrac_1(Igrac):
    def __init__(self, slika = "igrac1.png"):
        super().__init__(slika)
        self.prvi_igrac = True

class Igrac_2(Igrac):
    def __init__(self, slika = "igrac2.png"):
        super().__init__(slika)
        self.prvi_igrac = False

