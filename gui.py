from pygame.locals import *
import sys
from meni import *
from collections import OrderedDict

screen = pygame.display.set_mode((640,480))

pygame.init()

def napusti_igru():
    pygame.quit()
    sys.exit()

def pokreni_meni():
    while glavni_meni.aktivan:
        glavni_meni.draw()
        handle_menu_event(glavni_meni)
        pygame.display.update()


glavni_meni = Meni(
    screen, OrderedDict(
        [('Izadji', napusti_igru)]
    )
)

def handle_menu_event(glavni_meni):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            napusti_igru()
        elif event.type == MOUSEBUTTONUP:
            for option in glavni_meni.opcije:
                if option.is_selected:
                    if not isinstance(option.function, tuple):
                        option.function()
                    else:
                        option.function[0](option.function[1])
