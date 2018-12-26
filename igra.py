
class Igra:
    def __init__(self, nivo = 1):
        self.nivo = nivo
        self.dva_igraca = False
        self.lopte = []
        self.igraci = []  #igrac class
        self.skokovi = [] #sin(ax)
        self.zavrsena_igra = False
        self.predjen_nivo = False
        self.restartuj_nivo = False
        self.izgubljeni_zivoti = False

    def ucitaj_nivo(self, nivo):
        self.restartuj_nivo = True
        self.lopte = []
        self.skokovi = []
        self.izgubljeni_zivoti = False
        self.nivo = nivo
        self.predjen_nivo = False
        if self.dva_igraca and len(self.igraci) == 1:
            self.igraci.append()    #igrac class
        for index, igrac in enumerate(self.igraci):
            index_igraca = index + 1
            broj_igraca = len(self.igraci)
            #pozicija
            #ucitavnje levela
