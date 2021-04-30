import pygame as pg
import run
from settings import window, colors
g = run.Game()

class MenuSet:
    def __init__(self):
        pg.init()
        self.running = True
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.LT_KEY, self.RT_KEY = False, False
        self.DISPLAY_W, self.DISPLAY_H = window['WIDTH'], window['HEIGHT']
        self.display = pg.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pg.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = pg.font.get_default_font()
        self.main_menu = MainMenu(self)
        # self.volume = Volume(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.curr_menu.run_display = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.START_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colors['WHITE'])
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = - 200

    def draw_cursor(self):
        self.game.draw_text('*', 60, self.cursor_rect.x + 40, self.cursor_rect.y + 20)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Iniciar"
        self.iniciarx, self.iniciary = self.mid_w, self.mid_h + 20
        self.sairx, self.sairy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.iniciarx + self.offset + 20, self.iniciary - 7)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(colors['BLACK'])
            self.game.draw_text('O monitorado', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Iniciar Jogo", 40, self.iniciarx, self.iniciary)
            self.game.draw_text("Sair", 40, self.sairx, self.sairy + 30)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Iniciar':
                self.cursor_rect.midtop = (self.sairx + self.offset + 90, self.sairy + 23)
                self.state = 'Sair'
        elif self.game.UP_KEY:
            if self.state == 'Sair':
                self.cursor_rect.midtop = (self.iniciarx + self.offset + 20, self.iniciary - 7)
                self.state = 'Iniciar'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Iniciar':
                g.new()
                g.run()
            elif self.state == 'Sair':
                g.quit()
            self.run_display = False

