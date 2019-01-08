import time

from pygame.locals import *
from collections import OrderedDict
from meni import *
from igra import *

pygame.init()
pygame.mouse.set_visible(True)
screen = pygame.display.set_mode((SIRINA,VISINA))
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
    igra.pobednik = 0
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
    igra.pobednik = 0
    zapocni_igru_sa_dva_igraca()

def prikazi_kontole():
    glavni_meni.aktivan = False
    igra.pokrenuto = False
    slicica = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "kontroleNase.jpg"), (SIRINA, VISINA))
    screen.blit(slicica, (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)
    pokreni_meni()


def pokreni_turnir():
    print("kliknut turnir")

glavni_meni = Meni(
    screen, OrderedDict(
        [('1 igrac', jedan_igrac),
         ('2 igraca', dva_igraca),
         ('Kontorle', prikazi_kontole),
         ('Izadji', napusti_igru),
         ("Igraj turnir", pokreni_turnir)]

    )
)


def iscrtaj_loptu(lopta):
    screen.blit(lopta.slika, lopta.rect)

def iscrtaj_igraca(igrac):
    screen.blit(igrac.slika, igrac.rect)

def iscrtaj_oruzje(oruzje):
    screen.blit(oruzje.slika, oruzje.rect)

def iscrtaj_bonus(bonus):
    screen.blit(bonus.slika, bonus.rect)

def ispisi_poruku(poruka, boja, podesavanje_ispisa):
    labela = font.render(poruka, 1, boja)
    rect = labela.get_rect()
    rect.centerx = screen.get_rect().centerx
    rect.centery = screen.get_rect().centery + podesavanje_ispisa
    screen.blit(labela, rect)

def iscrtaj_vreme():
    timer = font.render(str(igra.preostalo_vreme), 1, (255,0,0))
    rect = timer.get_rect()
    rect.topleft = 62, 40
    screen.blit(timer, rect)


def iscrtaj_nivoe():
    level = font.render(str(igra.nivo),1,(255,0,0))
    rect = level.get_rect()
    rect.topright = SIRINA - 87 , 40
    screen.blit(level,rect)

def iscrtaj_zivote(igrac, prvi_igrac=True):
    if not igrac.prvi_igrac:
        slika_igraca = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "igrac2.png"), (20, 20)) #velicina, ne pozicija
    else:
        slika_igraca = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "igrac1.png"), (20, 20))
    rect = slika_igraca.get_rect()
    for broj_zivota in range(igrac.zivoti):
        if not prvi_igrac:
            screen.blit(slika_igraca, ((broj_zivota + 1) * 20 + 15, 100))
        else:
            screen.blit(
                slika_igraca,
                (SIRINA - (broj_zivota + 1) * 20 - rect.width - 25, 100)
            )

def iscrtaj_nivo():
    br_slike = igra.nivo % 8
    if br_slike == 0:
        br_slike += 8
    slika_nivoa = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "level" + str(br_slike) +".jpg"), (SIRINA, VISINA))
    #slika_nivoa = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "level0.jpg"),(SIRINA, VISINA))
    screen.fill((255, 255, 255))
    screen.blit(slika_nivoa, (0, 0))
    for lopta in igra.lopte:
        iscrtaj_loptu(lopta)
    for index, igrac in enumerate(igra.igraci):
        if igrac.oruzje.ziv:
            iscrtaj_oruzje(igrac.oruzje)
        iscrtaj_igraca(igrac)
        iscrtaj_zivote(igrac, index)
    for bonus in igra.bonusi:
        iscrtaj_bonus(bonus)
    iscrtaj_vreme()
    iscrtaj_nivoe()
    if igra.zavrsena_igra:
        ispisi_poruku('Game over!', (0, 0, 255), 0)
        pygame.display.update()
        #pygame.time.delay(3000)
        if igra.pobednik == 1:
            ispisi_poruku('Pobednik je prvi igrac!', (0, 0, 255),25)
        elif igra.pobednik == 2:
            ispisi_poruku('Pobednik je drugi igrac!', (0, 0, 255),25)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.mouse.set_visible(True)
        pokreni_meni()
    if igra.predjen_nivo:
        ispisi_poruku('Well done! Level completed!', (0, 0, 255), 0)
    if igra.restartuj_nivo:
        ispisi_poruku('Get ready!', (0, 0, 255), 0)

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
                        #screen.blit(igra.igraci[0].oruzje.slika, igra.igraci[0].oruzje.rect)
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
                            #screen.blit(igra.igraci[0].oruzje.slika,igra.igraci[0].oruzje.rect)
                    else:
                        if event.key == K_a:
                            igra.igraci[1].levo = True
                        elif event.key == K_d:
                            igra.igraci[1].desno = True
                        elif event.key == K_w and \
                               not igra.igraci[1].oruzje.ziv:
                            igra.igraci[1].pucaj()
                            #screen.blit(igra.igraci[1].oruzje.slika, igra.igraci[1].oruzje.rect)
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

