import sys
import random
from lopta import *
from igrac import *
from threading import Timer
from bonusi import *
from multiprocessing import Queue

queueIgra = Queue()
retQueueIgra = Queue()

#brojac_kolizija = 0
class Igra:
    def __init__(self, nivo = 1):
        self.nivo = nivo
        self.prvi_igrac = True
        self.drugi_igrac = True
        self.dva_igraca = True
        self.online = False
        self.lopte = []
        self.bonusi = []
        self.igraci = []
        self.turnir = False
        self.zavrsen_turnir = False
        self.zavrsena_igra = False
        self.predjen_nivo = False
        self.restartuj_nivo = False
        self.izgubljeni_zivoti = False
        self.pokrenuto = True
        self.preostalo_vreme = 0
        self.pobednik = 0
        self.brojac_kolizija = 0
        self.broj_nivoa = 1
        self.bonus_tip = "Nista"
        # self.queue = Queue()
        # self.retQueue = Queue()

    def ucitaj_nivo(self, nivo):
        self.restartuj_nivo = True
        # if self.dva_igraca and len(self.igraci) == 1:
        #     self.igraci.append(enemy)
        #     self.igraci[1].prvi_igrac = False
        #     self.drugi_igrac = True
        self.lopte = []
        self.bonusi = []
        self.izgubljeni_zivoti = False  #dead_player
        for index, igrac in enumerate(self.igraci):
            index_igraca = index + 1
            broj_igraca = len(self.igraci)
            igrac.pocetna_pozicija(
                (640 / (broj_igraca + 1)) * index_igraca
            )
            igrac.ziv = True
        self.nivo = nivo
        self.predjen_nivo = False
        self._set_nivo(nivo)
        self._start_timer()

    def _start_timer(self):
        self._timer(1, self._tick_second, self.preostalo_vreme)


    def _check_for_collisions(self):
        for igrac in self.igraci:
            self._check_for_bubble_collision(self.lopte, igrac)
            self._check_for_bonus_collision(igrac)


    def _check_for_bubble_collision(self, loptice, igrac):
        global queueIgra
        for index, loptica in enumerate(loptice):
            if pygame.sprite.collide_rect(loptica, igrac.oruzje) \
                    and igrac.oruzje.ziv:
                igrac.oruzje.ziv = False
                self.brojac_kolizija += 1
                print("doslo do ovde")
                queueIgra.put(self.brojac_kolizija)
                self._split_ball(index)
                return True
            if pygame.sprite.collide_rect(loptica, igrac):  #collide_mask
                igrac.ziv = False
                self._decrease_lives(igrac)
                self._proveri_zivote()
                return True
        return False

    def _check_for_bonus_collision(self, igrac):
        for bonus_index, bonus in enumerate(self.bonusi):
            if pygame.sprite.collide_rect(bonus, igrac):
                self._activate_bonus(bonus.tip, igrac)
                del self.bonusi[bonus_index]
                return True
        return False

    def _decrease_lives(self, igrac):
        igrac.zivoti -= 1
        if igrac.zivoti:
            self.izgubljeni_zivoti = True
            igrac.ziv = False
        else:
            if igrac.prvi_igrac == True:
                self.prvi_igrac = False
                if self.dva_igraca:
                    self.pobednik = 2
            else:
                self.drugi_igrac = False
                if self.dva_igraca:
                    self.pobednik = 1
            self.igraci.remove(igrac)
            self.dva_igraca = False
            if self.igraci:
                self.restartuj_nivo = True
                self.restart()
            else:
                self.zavrsena_igra = True

    def _proveri_zivote(self):
        provera = False
        for index in self.igraci:
            if index.zivoti > 0:
                provera = True
        if not provera:
            self.zavrsena_igra = True


    def restart(self):
        self.ucitaj_nivo(self.nivo)



    def _activate_bonus(self, bonus, igrac):
        if bonus == BONUS_ZIVOT:
            if igrac.zivoti < 5:
                igrac.zivoti += 1
        elif bonus == BONUS_VREME:
            self.preostalo_vreme += 10

    def _split_ball(self, index_loptice):
        global retQueueIgra
        lopta = self.lopte[index_loptice]
        if lopta.velicina > 1:
            self.lopte.append(Lopta(lopta.rect.left - lopta.velicina ** 2, lopta.rect.top -10, lopta.velicina - 1,[-3, -math.fabs(math.sin((lopta.velicina-1)*3))]))
            self.lopte.append(Lopta(lopta.rect.left + lopta.velicina ** 2, lopta.rect.top -10, lopta.velicina - 1,[3, -math.fabs(math.sin((lopta.velicina-1)*3))]))
        del self.lopte[index_loptice]
        print("doslo i do ovdee")
        self.bonus_tip =retQueueIgra.get()
        print(self.bonus_tip) #ovde staneee zakuca
        if not self.bonus_tip == "Nista":
            bonus = Bonus(lopta.rect.centerx, lopta.rect.centery, self.bonus_tip)
            self.bonusi.append(bonus)
            self._timer(1, self._ukloni_bonus_ako_nije_uhvacen, bonus.preostalo_vreme)

    def azuriraj(self):
        if self.predjen_nivo:
            self.ucitaj_nivo(self.nivo + 1)
        if self.zavrsena_igra:
            self.pokrenuto = False
        if self.izgubljeni_zivoti:
            self.restart()
        self._check_for_collisions()
        for lopta in self.lopte:
            lopta.azuriraj()
        for igrac in self.igraci:
            igrac.azuriraj()
        for bonus in self.bonusi:
            bonus.azuriraj()
        if not self.lopte:
            self.predjen_nivo = True


    def _timer(self, interval, worker_func, iterations=0):
        if self.preostalo_vreme and not self.izgubljeni_zivoti and not \
                self.predjen_nivo and not self.restartuj_nivo:
            Timer(

                interval, self._timer,
                [interval, worker_func, 0 if self.preostalo_vreme ==
                    0 else iterations - 1]
            ).start()
            worker_func()

    def _tick_second(self):
        self.preostalo_vreme -= 1
        if self.preostalo_vreme == 0:
            for igrac in self.igraci:
                self._decrease_lives(igrac)

    def _ukloni_bonus_ako_nije_uhvacen(self):
        for bonus_index, bonus in enumerate(self.bonusi):
            bonus.preostalo_vreme -= 1
            if bonus.preostalo_vreme == 0:
                del self.bonusi[bonus_index]

    def _set_nivo(self, nivo):
        velicina = nivo % 4
        if velicina == 0:
            velicina+=4
        br_lopti = nivo//4
        if not nivo % 4 == 0:
            br_lopti += 1
        vreme = nivo + 19
        x = 200
        y = 200
        self.preostalo_vreme = vreme
        #x = 100
        for i in range(1, br_lopti+1):

            #y = x/2 * math.fabs(math.sin(x)) + velicina
            #y = int(y)
            self.lopte.append(Lopta(x, y, velicina, [3, 1])) #velicina * math.fabs(math.sin(3))
            x-=30
            y-=30

def _drop_bonus(queueIgra, retQueueIgra):
    #global retQueueIgra
    bonus_tip = None
    while True:
        rr = queueIgra.get()
        if not rr == "Izadji":
            brojac_kol = rr
            if brojac_kol % 5 == 0:
                bonus_tip = BONUS_VREME
            elif brojac_kol % 11 == 0:
                bonus_tip = BONUS_ZIVOT
            else:
                bonus_tip = "Nista"
            retQueueIgra.put(bonus_tip)
        else:
            print("izlazi iz treceg procesa")
            pygame.quit()
            sys.exit()
            break
