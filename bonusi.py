import pygame

from konfiguracija import *

BONUS_ZIVOT = 'bonus life'
BONUS_VREME = 'bonus time'

bonus_tipovi = [BONUS_ZIVOT, BONUS_VREME]


class Bonus(pygame.sprite.Sprite):
    def __init__(self, x, y, tip):
        self.slika = pygame.image.load(PUTANJA_SLIKE + tip + '.png')
        self.rect = self.slika.get_rect(centerx=x, centery=y)
        self.tip = tip

    def azuriraj(self):
        if self.rect.bottom < VISINA:
            self.rect = self.rect.move(0, 2)