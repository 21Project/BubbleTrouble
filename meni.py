import pygame

class MeniOpcija (pygame.font.Font):
    def __init__(self, text, function,
                 position=(0, 0), font=None, font_size=36, font_color=(255,255,255)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.function = function
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, font_color)
        self.rect = self.label.get_rect(left=position[0], top=position[1])
        self.position = position
        self.is_selected = False

    def set_position(self, x, y):
        self.position = (x, y)
        self.rect = self.label.get_rect(left=x, top=y)

    def highlight(self, color=(255,0,0)):
        self.font_color = color
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = True

    def unhighlight(self):
        self.font_color = (255,255,255)
        self.label = self.render(self.text, 1, self.font_color)
        self.is_selected = False

    def check_for_mouse_selection(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.highlight()
        else:
            self.unhighlight()


class Meni():
    def __init__(self, screen, funkcije,bg_color = (0,0,0)):
        self.aktivan = True
        self.screen = screen
        self.bg_color = bg_color
        self.sirina_prozora = self.screen.get_rect().width
        self.visina_prozora = self.screen.get_rect().height
        self.opcije = []
        self.trenutna_opcija = None
        self.funkcije = funkcije
        for index, opcija in enumerate(funkcije.keys()):
            meni_opcija = MeniOpcija(opcija, funkcije[opcija])
            sirina = meni_opcija.rect.width
            visina = meni_opcija.rect.height
            maksimalna_visina = len(funkcije) * visina
            pos_x = self.sirina_prozora / 2 - sirina / 2
            pos_y = self.visina_prozora / 2 - maksimalna_visina / 2 + index * visina
            if meni_opcija.text == 'Back':
                meni_opcija.set_position(20, self.visina_prozora - 40)
            else:
                meni_opcija.set_position(pos_x, pos_y)
            self.opcije.append(meni_opcija)

    def draw(self):
        self.screen.fill(self.bg_color)
        for option in self.opcije:
            option.check_for_mouse_selection(pygame.mouse.get_pos())
            if self.trenutna_opcija is not None:
                self.opcije[self.trenutna_opcija].highlight()
            self.screen.blit(option.label, option.position)


