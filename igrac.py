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
        self.prvi_igrac = True

    def pucaj(self):
        self.oruzje = Oruzje(self.rect.centerx, self.rect.top)
        #print(self.rect.centerx)
        #print(self.rect.top)
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