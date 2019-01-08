import sys
import random
from lopta import *
from igrac import *
from threading import Timer
from bonusi import *

class Igra:
    def __init__(self, nivo = 1):
        self.nivo = nivo
        self.prvi_igrac = True
        self.drugi_igrac = False
        self.dva_igraca = False
        self.lopte = []
        self.bonusi = []
        if DVA_IGRACA:
            self.igraci = [me]
        else:
            self.igraci = [Igrac_1()]
        self.zavrsena_igra = False
        self.predjen_nivo = False
        self.restartuj_nivo = False
        self.izgubljeni_zivoti = False
        self.pokrenuto = True
        self.preostalo_vreme = 0
        self.pobednik = 0

    def ucitaj_nivo(self, nivo):
        self.restartuj_nivo = True
        if self.dva_igraca and len(self.igraci) == 1:
            self.igraci.append(enemy)
            self.igraci[1].prvi_igrac = False
            self.drugi_igrac = True
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
        for index, loptica in enumerate(loptice):
            if pygame.sprite.collide_rect(loptica, igrac.oruzje) \
                    and igrac.oruzje.ziv:
                igrac.oruzje.ziv = False
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

    @staticmethod
    def _drop_bonus():
        if random.randrange(BONUS_DROP_RATE) == 0:
            bonus_tip = random.choice(bonus_tipovi)
            return bonus_tip

    def _activate_bonus(self, bonus, igrac):
        if bonus == BONUS_ZIVOT:
            if igrac.zivoti < 5:
                igrac.zivoti += 1
        elif bonus == BONUS_VREME:
            self.preostalo_vreme += 10

    def _split_ball(self, index_loptice):
        lopta = self.lopte[index_loptice]
        if lopta.velicina > 1:
            # print("bottom1 " + str(self.lopte[index_loptice].rect.bottom))
            # print("top1 " + str(self.lopte[index_loptice].rect.top))
            #print("igrac top" + str(self.igraci[0].rect.top))
            #print("igrac bottom" + str(self.igraci[0].rect.bottom))

            # if lopta.rect.bottom < 440:
            #     print("udji u if")
            #     self.lopte.append(Lopta(lopta.rect.left - lopta.velicina ** 2, lopta.rect.top - 60, lopta.velicina - 1,
            #                             [-3, -(lopta.velicina - 1) * math.fabs(math.sin(3))]))
            #     self.lopte.append(Lopta(lopta.rect.left + lopta.velicina ** 2, lopta.rect.top - 60, lopta.velicina - 1,
            #                             [3, -(lopta.velicina - 1) * math.fabs(math.sin(3))]))
            # else:
            #print("udji u else")


            self.lopte.append(Lopta(lopta.rect.left - lopta.velicina ** 2, lopta.rect.top -10, lopta.velicina - 1,[-3, 1]))
            self.lopte.append(Lopta(lopta.rect.left + lopta.velicina ** 2, lopta.rect.top -10, lopta.velicina - 1,[3, (lopta.velicina - 1) * math.fabs(math.sin(3))]))

            # ovo valja self.lopte.append(Lopta(lopta.rect.left - lopta.velicina**2,lopta.rect.top - 10, lopta.velicina - 1, [-3, -(lopta.velicina-1) * math.fabs(math.sin(3))]))
            #self.lopte.append(Lopta(lopta.rect.left - lopta.velicina ** 2, lopta.rect.top - 10, lopta.velicina - 1,[-3, -(lopta.velicina - 1) * math.fabs(math.sin(3))]))
            # ovo valja self.lopte.append(Lopta(lopta.rect.left + lopta.velicina ** 2, lopta.rect.top - 10, lopta.velicina - 1,[3, -(lopta.velicina - 1) * math.fabs(math.sin(3))]))
            # self.lopte.insert(len(self.lopte),Lopta(lopta.rect.left - lopta.velicina**2,lopta.rect.top - 100, lopta.velicina - 1, [-3, -(lopta.velicina-1) * math.fabs(math.sin(3))]))
            # self.lopte.insert(len(self.lopte),Lopta(lopta.rect.left + lopta.velicina**2,lopta.rect.top - 100, lopta.velicina - 1, [3, -(lopta.velicina-1) * math.fabs(math.sin(3))]))
            # print("bottom " + str(self.lopte[len(self.lopte)-1].rect.bottom))
            # print("top " + str(self.lopte[len(self.lopte)-1].rect.top))
        del self.lopte[index_loptice]
        bonus_tip = self._drop_bonus()
        if bonus_tip:
            bonus = Bonus(lopta.rect.centerx, lopta.rect.centery, bonus_tip)
            self.bonusi.append(bonus)



    def azuriraj(self):
        if self.predjen_nivo:
            self.ucitaj_nivo(self.nivo + 1)
        if self.zavrsena_igra:
            self.pokrenuto = False
            #pygame.quit()
            #sys.exit()
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
        if iterations and not self.izgubljeni_zivoti and not \
                self.predjen_nivo and not self.restartuj_nivo:
            Timer(

                interval, self._timer,
                [interval, worker_func, 0 if iterations ==
                    0 else iterations - 1]
            ).start()
            worker_func()

    def _tick_second(self):
        self.preostalo_vreme -= 1
        if self.preostalo_vreme == 0:
            for igrac in self.igraci:
                self._decrease_lives(igrac)

    def _set_nivo(self, nivo):
        velicina = nivo % 4
        if velicina == 0:
            velicina+=4
        br_lopti = nivo//4
        if not nivo % 4 == 0:
            br_lopti += 1
        vreme = nivo + 19
        x = 200
        y = 250
        self.preostalo_vreme = vreme
        #x = 100
        for i in range(1, br_lopti+1):

            #y = x/2 * math.fabs(math.sin(x)) + velicina
            #y = int(y)
            self.lopte.append(Lopta(x, y, velicina, [3, 1])) #velicina * math.fabs(math.sin(3))
            x-=30
            y-=30
