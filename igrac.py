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

    def pucaj(self):
        self.oruzje = Oruzje(self.rect.centerx, self.rect.top)
        self.oruzje.ziv = True

    def azuriraj(self):
        if self.levo and self.rect.left >= 0:
            self.rect = self.rect.move(-5, 0)
        if self.desno and self.rect.right <= 640:
            self.rect = self.rect.move(5, 0)
        if self.oruzje.ziv:
            self.oruzje.azuriraj()

    def pocetna_pozicija(self, x = 320, y = 480):
        self.rect.centerx, self.rect.bottom = x, y
        self.oruzje.ziv = False