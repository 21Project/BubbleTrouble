import pygame
import math

from konfiguracija import *

class Lopta(pygame.sprite.Sprite):
    def __init__(self, x, y, velicina, brzina, naziv_slike = "lopta.png"):
        pygame.sprite.Sprite.__init__(self)
        self.slika = pygame.image.load(PUTANJA_SLIKE + naziv_slike)
        self.slika = pygame.transform.scale(self.slika, (velicina*15, velicina*15))
        self.rect = self.slika.get_rect(centerx=x, centery=y)
        self.velicina = velicina
        self.brzina = brzina




    def azuriraj(self):
        self.brzina[1] += 1  # gravity
        self.rect = self.rect.move(self.brzina)
        if self.rect.left < 30 or self.rect.right > SIRINA - 35:
            self.brzina[0] = -self.brzina[0]
        if self.rect.top < 95 or self.rect.bottom > VISINA:
            self.brzina[1] = -self.brzina[1]

        self.rect.left = self._clip(self.rect.left, 0, SIRINA)
        self.rect.right = self._clip(self.rect.right, 0, SIRINA)
        self.rect.top = self._clip(self.rect.top, 95, VISINA)
        self.rect.bottom = self._clip(self.rect.bottom, 0, VISINA)



    @staticmethod
    def _clip(val, min_value, max_value):
        return min(max(val, min_value), max_value)
