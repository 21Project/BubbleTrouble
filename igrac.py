from oruzje import *

class Igrac(pygame.sprite.Sprite):
    def __init__(self, slika = "igrac1.png"):
        self.slika = pygame.image.load(PUTANJA_SLIKE + slika)
        self.rect = self.slika.get_rect()
        self.desno = False
        self.levo = False
        self.oruzje = Oruzje()
        self.zivoti = 3
        self.pocetna_pozicija()
        self.ziv = True

    def pocetna_pozicija(self, x = 320, y = 480):
        self.rect.centerx, self.rect.bottom = x, y
        self.oruzje.ziv = False