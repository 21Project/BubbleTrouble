from pygame.locals import *
from collections import OrderedDict
from meni import *
from igra import *

pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 30)
igra = Igra()

def start_nivo(nivo):
    igra.ucitaj_nivo(nivo)
    glavni_meni.aktivan = False
    pygame.mouse.set_visible(False)
    while igra.pokrenuto:
        igra.azuriraj()
        iscrtaj_nivo()
        handle_game_event()
        pygame.display.update()
        # if igra.zavrsena_igra:
        #     print("uslo u if za zavrsena_igra")
        if igra.predjen_nivo or igra.restartuj_nivo:
            pygame.time.delay(2000)
        if igra.izgubljeni_zivoti:
            pygame.time.delay(1000)
        if igra.restartuj_nivo:
            igra.restartuj_nivo = False
            igra._start_timer()
        clock.tick(30)


def pokreni_meni():
    glavni_meni.aktivan = True
    igra.pokrenuto = False
    while glavni_meni.aktivan:
        glavni_meni.draw()
        handle_menu_event(glavni_meni)
        pygame.display.update()
        clock.tick(30)


def zapocni_igru_sa_jednim_igracem():
    brojac = 1
    while True:
        if not igra.zavrsena_igra:
            #igra.nivo = brojac
            start_nivo(brojac)
            brojac+=1
            clock.tick(30)
        else:
            break

   # ucitan_level.aktivan = True
    #while ucitan_level.aktivan:
       # ucitan_level.draw()
        #handle_menu_event(ucitan_level)
       # pygame.display.update()
        #clock.tick(FPS)

def zapocni_igru_sa_dva_igraca():
    brojac = 1
    while True:
        if not igra.zavrsena_igra:
            start_nivo(brojac)
            brojac+=1
            clock.tick(30)
        else:
            break


def napusti_igru():
    pygame.quit()
    sys.exit()


def jedan_igrac():
    igra.pokrenuto = True
    igra.zavrsena_igra = False
    igra.prvi_igrac = True
    igra.drugi_igrac = False
    igra.dva_igraca = True
    igra.igraci = [Igrac()]
    igra.lopte = []
    igra.predjen_nivo = False
    igra.restartuj_nivo = False
    igra.izgubljeni_zivoti = False
    igra.preostalo_vreme = 0
    igra.dva_igraca = False
    zapocni_igru_sa_jednim_igracem()


def dva_igraca():
    igra.pokrenuto = True
    igra.zavrsena_igra = False
    igra.prvi_igrac = True
    igra.drugi_igrac = False
    igra.dva_igraca = True
    igra.igraci = [Igrac()]
    igra.lopte = []
    igra.predjen_nivo = False
    igra.restartuj_nivo = False
    igra.izgubljeni_zivoti = False
    igra.preostalo_vreme = 0
    igra.dva_igraca = True
    zapocni_igru_sa_dva_igraca()


glavni_meni = Meni(
    screen, OrderedDict(
        [('Izadji', napusti_igru),
         ('1 igrac', jedan_igrac),
         ('2 igraca', dva_igraca)]
    )
)


#ucitan_level = Meni(screen, OrderedDict("level"))

def iscrtaj_loptu(lopta):
    screen.blit(lopta.slika, lopta.rect)

def iscrtaj_igraca(igrac):
    screen.blit(igrac.slika, igrac.rect)

def iscrtaj_oruzje(oruzje):
    screen.blit(oruzje.slika, oruzje.rect)


def ispisi_poruku(poruka, boja):
    labela = font.render(poruka, 1, boja)
    rect = labela.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery
    screen.blit(labela, rect)

def iscrtaj_vreme():
    timer = font.render(str(igra.preostalo_vreme), 1, (255,0,0))
    rect = timer.get_rect()
    rect.bottomleft = 10, 480 - 10
    screen.blit(timer, rect)

def iscrtaj_nivoe():
    level = font.render(str(igra.nivo),1,(255,0,0))
    rect = level.get_rect()
    rect.bottomright = 640 - 10 ,480 -10
    screen.blit(level,rect)

def iscrtaj_zivote(igrac, prvi_igrac=True):
    slika_igraca = pygame.transform.scale(igrac.slika, (20, 20))
    rect = slika_igraca.get_rect()
    for broj_zivota in range(igrac.zivoti):
        if not prvi_igrac:
            screen.blit(slika_igraca, ((broj_zivota + 1) * 20, 10))
        else:
            screen.blit(
                slika_igraca,
                (640 - (broj_zivota + 1) * 20 - rect.width, 10)
            )

def iscrtaj_nivo():
    screen.fill((255, 255, 255))
    for lopta in igra.lopte:
        iscrtaj_loptu(lopta)
    for index, igrac in enumerate(igra.igraci):
        if igrac.oruzje.ziv:
            iscrtaj_oruzje(igrac.oruzje)
        iscrtaj_igraca(igrac)
        iscrtaj_zivote(igrac, index)
    iscrtaj_vreme()
    iscrtaj_nivoe()
    if igra.zavrsena_igra:
        ispisi_poruku('Game over!', (0, 0, 255))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.mouse.set_visible(True)
        #igra.pokrenuto = False
        #glavni_meni.aktivan =True
        pokreni_meni()
    if igra.predjen_nivo:
        ispisi_poruku('Well done! Level completed!', (0, 0, 255))
    if igra.restartuj_nivo:
        ispisi_poruku('Get ready!', (0, 0, 255))

def handle_game_event():
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if igra.prvi_igrac:
                    if event.key == K_LEFT:
                        igra.igraci[0].levo = True
                    elif event.key == K_RIGHT:
                        igra.igraci[0].desno = True
                    elif event.key == K_SPACE and not igra.igraci[0].oruzje.ziv:
                        igra.igraci[0].pucaj()
                    elif event.key == K_ESCAPE:
                        napusti_igru()
                if igra.drugi_igrac:
                    if igra.prvi_igrac == False:
                        if event.key == K_a:
                            igra.igraci[0].levo = True
                        elif event.key == K_d:
                            igra.igraci[0].desno = True
                        elif event.key == K_w and \
                                not igra.igraci[0].oruzje.ziv:
                            igra.igraci[0].pucaj()
                    else:
                        if event.key == K_a:
                            igra.igraci[1].levo = True
                        elif event.key == K_d:
                            igra.igraci[1].desno = True
                        elif event.key == K_w and \
                               not igra.igraci[1].oruzje.ziv:
                            igra.igraci[1].pucaj()
            if event.type == KEYUP:
                if igra.prvi_igrac:
                    if event.key == K_LEFT:
                        igra.igraci[0].levo = False
                    elif event.key == K_RIGHT:
                        igra.igraci[0].desno = False
                if igra.drugi_igrac:
                    if igra.prvi_igrac == False:
                        if event.key == K_a:
                            igra.igraci[0].levo = False
                        elif event.key == K_d:
                            igra.igraci[0].desno = False
                    else:
                        if event.key == K_a:
                            igra.igraci[1].levo = False
                        elif event.key == K_d:
                            igra.igraci[1].desno = False
            if event.type == QUIT:
                napusti_igru()

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

