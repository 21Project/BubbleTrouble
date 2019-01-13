from igra import *
from meni import *
from pygame.locals import *
from collections import OrderedDict

from multiprocessing import Process, Queue

#pygame.init()
igra = None

njegova_adresa = ''
njegov_port = 0
moja_adresa = ''
moj_port = 0

me_igrac1 = None
me = None
enemy = None
server = None


class Gui():
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 30)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SIRINA, VISINA))
        self.glavni_meni = self.dodeli_meni()
        self.queue = Queue()
        self.retQueue = Queue()

    def start_nivo(self,nivo):
        igra.ucitaj_nivo(nivo)
        self.glavni_meni.aktivan = False
        pygame.mouse.set_visible(False)
        while igra.pokrenuto:
            igra.azuriraj()
            self.iscrtaj_nivo()
            self.handle_game_event()
            if igra.online:
                self.data_transfer(me, enemy, server)
            pygame.display.update()
            if igra.predjen_nivo or igra.restartuj_nivo:
                if igra.online:
                    if me.ziv:
                        me.levo = False
                        me.desno = False
                        me.oruzje.ziv = False
                    if enemy.ziv:
                        enemy.levo = False
                        enemy.desno = False
                        enemy.oruzje.ziv = False
                pygame.time.delay(2000)
            if igra.izgubljeni_zivoti:
                pygame.time.delay(1000)
            if igra.restartuj_nivo:
                igra.restartuj_nivo = False
                igra._start_timer()
            self.clock.tick(30)


    def pokreni_meni(self):
        self.glavni_meni.aktivan = True
        while self.glavni_meni.aktivan:
            self.glavni_meni.draw()
            self.handle_menu_event(self.glavni_meni)
            pygame.display.update()
            self.clock.tick(30)


    def zapocni_igru(self):
        global queue
        global retQueue

        while True:
            if not igra.zavrsena_igra:
                self.start_nivo(igra.broj_nivoa)
                queue.put(True)
                self.clock.tick(30)
            else:
                queue.put(False)
                break


    def napusti_igru(self):
        print("napusti_igru")
        pygame.quit()
        sys.exit()


    def dva_igraca(self):
        global igra
        igra = Igra()
        igra.online = True
        global njegova_adresa
        global njegov_port
        global moja_adresa
        global moj_port
        moj_port = 0
        njegov_port = 0
        njegova_adresa, njegov_port, moja_adresa, moj_port = client_connect_function("dva_igraca")
        if not moj_port == 0 and not njegov_port == 0:
            self.pokreni_igru()


    def offline_dva_igraca(self):
        global  igra
        igra = Igra()
        igra.online = False
        igra.igraci = [Igrac_1()]
        igra.igraci.append(Igrac_2())
        self.zapocni_igru()

    def jedan_igrac(self):
        global igra
        igra = Igra()
        igra.online = False
        igra.dva_igraca = False
        igra.drugi_igrac = False
        igra.igraci = [Igrac_1()]
        self.zapocni_igru()

    def prikazi_kontrole(self):
        print("prikazi_kontrole")
        self.glavni_meni.aktivan = False
        slicica = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "kontroleNase.jpg"), (SIRINA, VISINA))
        self.screen.blit(slicica, (0, 0))
        pygame.display.update()
        pygame.time.delay(3000)
        self.pokreni_meni()


    def pokreni_turnir(self):
        print("pokreni_turnir")
        global igra
        igra = Igra()
        igra.online = True
        igra.turnir = True
        global njegova_adresa
        global njegov_port
        global moja_adresa
        global moj_port
        moj_port = 0
        njegov_port = 0
        njegova_adresa, njegov_port, moja_adresa, moj_port = client_connect_function("igraj_turnir")
        if not moj_port == 0 and not njegov_port == 0:
            self.pokreni_igru()

    def data_transfer(self,me, enemy, server):
        me_data = me.make_data_package()
        send(me_data, njegova_adresa, njegov_port)  # the send code

        enemy_data = server.receive()  # the receive code

        enemy.rect.centerx = int(enemy_data[:4])
        enemy.rect.centery = int(enemy_data[4:8])
        if len(enemy_data) > 8:
            enemy.oruzje.ziv = True
            enemy.oruzje.rect.centerx = int(enemy_data[8:12])
            enemy.oruzje.rect.centery = int(enemy_data[12:16])


    def pokreni_igru(self):
        global me
        global enemy
        global me_igrac1
        me, enemy, me_igrac1 = define_players(moja_adresa, njegova_adresa)
        global server
        server = Server_igra(moja_adresa, moj_port)
        if me_igrac1:
            igra.igraci = [me]
            igra.igraci.append(enemy)
        else:
            igra.igraci = [enemy]
            igra.igraci.append(me)
        self.zapocni_igru()

    def dodeli_meni(self):
        glavni_meni = Meni(self.screen,
             OrderedDict(
                 [('1 igrac', self.jedan_igrac),
                  ('2 igraca-Offline', self.offline_dva_igraca),
                  ('2 igraca-Online', self.dva_igraca),
                  ("Igraj turnir", self.pokreni_turnir),
                  ('Izadji', self.napusti_igru),
                  ('Kontrole', self.prikazi_kontrole)]))
        return glavni_meni



    def iscrtaj_loptu(self,lopta):
        self.screen.blit(lopta.slika, lopta.rect)


    def iscrtaj_igraca(self,igrac):
        self.screen.blit(igrac.slika, igrac.rect)


    def iscrtaj_oruzje(self,oruzje):
        self.screen.blit(oruzje.slika, oruzje.rect)


    def iscrtaj_bonus(self,bonus):
        self.screen.blit(bonus.slika, bonus.rect)


    def ispisi_poruku(self,poruka, boja, podesavanje_ispisa):
        labela = self.font.render(poruka, 1, boja)
        rect = labela.get_rect()
        rect.centerx = self.screen.get_rect().centerx
        rect.centery = self.screen.get_rect().centery + podesavanje_ispisa
        self.screen.blit(labela, rect)


    def iscrtaj_vreme(self):
        timer = self.font.render(str(igra.preostalo_vreme), 1, (255, 0, 0))
        rect = timer.get_rect()
        rect.topleft = 62, 40
        self.screen.blit(timer, rect)


    def iscrtaj_nivoe(self):
        level = self.font.render(str(igra.nivo), 1, (255, 0, 0))
        rect = level.get_rect()
        rect.topright = SIRINA - 87, 40
        self.screen.blit(level, rect)


    def iscrtaj_zivote(self,igrac, prvi_igrac=True):
        if not igrac.prvi_igrac:
            slika_igraca = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "igrac2.png"),
                                                  (20, 20))  # velicina, ne pozicija
        else:
            slika_igraca = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "igrac1.png"), (20, 20))
        rect = slika_igraca.get_rect()
        for broj_zivota in range(igrac.zivoti):
            if not prvi_igrac:
                self.screen.blit(slika_igraca, ((broj_zivota + 1) * 20 + 15, 100))
            else:
                self.screen.blit(
                    slika_igraca,
                    (SIRINA - (broj_zivota + 1) * 20 - rect.width - 25, 100)
                )


    def iscrtaj_nivo(self):
        global njegova_adresa
        global njegov_port
        global moja_adresa
        global moj_port
        global igra
        global queue
        br_slike = igra.nivo % 8
        if br_slike == 0:
            br_slike += 8
        slika_nivoa = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "level" + str(br_slike) + ".jpg"),
                                             (SIRINA, VISINA))
        # slika_nivoa = pygame.transform.scale(pygame.image.load(PUTANJA_SLIKE + "level0.jpg"),(SIRINA, VISINA))
        self.screen.fill((255, 255, 255))
        self.screen.blit(slika_nivoa, (0, 0))
        for lopta in igra.lopte:
            self.iscrtaj_loptu(lopta)
        for index, igrac in enumerate(igra.igraci):
            if igrac.oruzje.ziv:
                self.iscrtaj_oruzje(igrac.oruzje)
            self.iscrtaj_igraca(igrac)
            self.iscrtaj_zivote(igrac, index)
        for bonus in igra.bonusi:
            self.iscrtaj_bonus(bonus)
        self.iscrtaj_vreme()
        self.iscrtaj_nivoe()
        if igra.zavrsena_igra:
            self.queue.put(False)
            self.ispisi_poruku('Game over!', (0, 0, 255), 0)

            pygame.display.update()
            # pygame.time.delay(3000)
            if igra.pobednik == 1:
                if igra.zavrsen_turnir:
                    self.ispisi_poruku('Pobednik turnira je prvi igrac!', (0, 0, 255), 25)
                    pygame.display.update()
                    pygame.time.delay(1000)
                else:
                    self.ispisi_poruku('Pobednik je prvi igrac!', (0, 0, 255), 25)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    if igra.turnir:
                        if me_igrac1:
                            moj_port = 0
                            njegov_port = 0
                            njegova_adresa, njegov_port, moja_adresa, moj_port = client_connect_function("pobednik_partije")
                            igra = Igra()
                            igra.online = True
                            igra.zavrsen_turnir = True
                            if not moj_port == 0 and not njegov_port ==0:
                                self.pokreni_igru()
            elif igra.pobednik == 2:
                if  igra.zavrsen_turnir:
                    self.ispisi_poruku('Pobednik turnira je drugi igrac!', (0, 0, 255), 25)
                    pygame.display.update()
                    pygame.time.delay(1000)
                else:
                    self.ispisi_poruku('Pobednik je drugi igrac!', (0, 0, 255), 25)
                    pygame.display.update()
                    pygame.time.delay(1000)
                    if igra.turnir:
                        if not me_igrac1:
                            moj_port = 0
                            njegov_port =0
                            njegova_adresa, njegov_port, moja_adresa, moj_port = client_connect_function("pobednik_partije")
                            igra = Igra()
                            igra.online = True
                            igra.zavrsen_turnir = True
                            if not moj_port == 0 and not njegov_port ==0:
                                self.pokreni_igru()

            pygame.display.update()
            pygame.time.delay(2000)
            pygame.mouse.set_visible(True)
            self.pokreni_meni()
        if igra.predjen_nivo:
            self.ispisi_poruku('Well done! Level completed!', (0, 0, 255), 0)
        if igra.restartuj_nivo:
            self.ispisi_poruku('Get ready!', (0, 0, 255), 0)


    def handle_game_event(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if not igra.online:
                    if igra.prvi_igrac:
                        if event.key == K_LEFT:
                            igra.igraci[0].levo = True
                        elif event.key == K_RIGHT:
                            igra.igraci[0].desno = True
                        elif event.key == K_SPACE and not igra.igraci[0].oruzje.ziv:
                            igra.igraci[0].pucaj()
                            # screen.blit(igra.igraci[0].oruzje.slika, igra.igraci[0].oruzje.rect)
                        elif event.key == K_ESCAPE:
                            self.napusti_igru()
                    if igra.drugi_igrac:
                        if igra.prvi_igrac == False:
                            if event.key == K_a:
                                igra.igraci[0].levo = True
                            elif event.key == K_d:
                                igra.igraci[0].desno = True
                            elif event.key == K_w and \
                                    not igra.igraci[0].oruzje.ziv:
                                igra.igraci[0].pucaj()
                                # screen.blit(igra.igraci[0].oruzje.slika,igra.igraci[0].oruzje.rect)
                        else:
                            if event.key == K_a:
                                igra.igraci[1].levo = True
                            elif event.key == K_d:
                                igra.igraci[1].desno = True
                            elif event.key == K_w and \
                                    not igra.igraci[1].oruzje.ziv:
                                igra.igraci[1].pucaj()
                                # screen.blit(igra.igraci[1].oruzje.slika, igra.igraci[1].oruzje.rect)
                else:
                    if me.ziv:
                        if igra.igraci[0] == me:
                            if event.key == K_LEFT:
                                igra.igraci[0].levo = True
                            elif event.key == K_RIGHT:
                                igra.igraci[0].desno = True
                            elif event.key == K_SPACE and not igra.igraci[0].oruzje.ziv:
                                igra.igraci[0].pucaj()
                                # screen.blit(igra.igraci[0].oruzje.slika, igra.igraci[0].oruzje.rect)
                            elif event.key == K_ESCAPE:
                                self.napusti_igru()
                        elif igra.igraci[1] == me:
                            if event.key == K_LEFT:
                                igra.igraci[1].levo = True
                            elif event.key == K_RIGHT:
                                igra.igraci[1].desno = True
                            elif event.key == K_SPACE and not igra.igraci[1].oruzje.ziv:
                                igra.igraci[1].pucaj()
                                # screen.blit(igra.igraci[0].oruzje.slika, igra.igraci[0].oruzje.rect)
                            elif event.key == K_ESCAPE:
                                self.napusti_igru()

            if event.type == KEYUP:
                if not igra.online:
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
                else:
                    if me.ziv:
                        if igra.igraci[0] == me:
                            if event.key == K_LEFT:
                                igra.igraci[0].levo = False
                            elif event.key == K_RIGHT:
                                igra.igraci[0].desno = False
                        elif igra.igraci[1] == me:
                            if event.key == K_LEFT:
                                igra.igraci[1].levo = False
                            elif event.key == K_RIGHT:
                                igra.igraci[1].desno = False
            if event.type == QUIT:
                self.napusti_igru()


    def handle_menu_event(self,glavni_meni):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.napusti_igru()
            elif event.type == MOUSEBUTTONUP:
                for option in glavni_meni.opcije:
                    if option.is_selected:
                        if not isinstance(option.function, tuple):
                            option.function()
                        else:
                            option.function[0](option.function[1])

    def run_game(self):
        p1 = Process(target=broj_nivoe, args=[self.queue])
        p1.start()
        self.pokreni_meni()

def broj_nivoe(queue):
    brojac = 0
    while True:
        message = queue.get()
        if message:
            brojac +=1
            igra.broj_nivoa = brojac
        else:
            break
            pygame.quit()
            sys.exit()

