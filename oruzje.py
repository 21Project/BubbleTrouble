import pygame
from konfiguracija import *

class Oruzje(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0):
        self.ziv = False
        pygame.sprite.Sprite.__init__(self)
        self.slika = pygame.image.load(PUTANJA_SLIKE + "strelica.png")
        self.rect = self.slika.get_rect(centerx = x, top = y)

    def azuriraj(self):
        if self.ziv:
            if self.rect.top <= 103:
                self.ziv = False
            else:
                self.rect = self.rect.move(0, -15)