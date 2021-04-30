from moviepy.editor import *
import pygame as pg
import numpy as np

import sys
import os
from random import choices
from time import time

import menu
from settings import window, options, colors
from sprites import Player, Obstacle, Scroll
from map_tile import TiledMap, Map, Camera, load_occupation_map

def video():
    '''
    introduction video
    '''
    pg.display.set_caption('O monitorado')
    clip = VideoFileClip('projeto.mp4')
    clip.preview()


class Game:
    '''
    '''
    def __init__(self):
        # Window
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 30'
        pg.init()
        self.screen = pg.display.set_mode((window['WIDTH'], window['HEIGHT']))
        self.screen.fill(colors['DARK_GREY'])
        pg.display.set_caption(window['TITLE'])
        pg.display.set_icon(window['GAME_LOGO'])

        # Clock
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.t0 = time()
        self.elapsed = 0
        self.maxTime = 288  # 288 = 48 hrs (game world)

        # Data and Map
        self.load_data()
        self.scrollCollected = True
        self.openSet = self.get_open_coordinates(os.path.join(self.map_folder, 'openSet.npy'))

        # Music
        self.current_song = -1
        pg.mixer.music.set_volume(0.5)

        # Text
        self.font = pg.font.Font("C:\Windows\Fonts\Courbd.ttf", 14)

        # Others
        self.cheat = 0

    def load_data(self):
        '''
        Loading Data from folders
        '''
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'Assets/Images')
        self.audio_folder = os.path.join(self.game_folder, 'Assets/Audio')
        self.songs = [os.path.join(self.audio_folder, f'track-{i}.mp3') for i in range(1, 4)]
        self.map_folder = os.path.join(self.game_folder, 'Tile Map')
        self.map = TiledMap(os.path.join(self.map_folder, 'Map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(os.path.join(self.img_folder, options['PLAYER_IMG'])).convert_alpha()
        self.wall_img = pg.image.load(os.path.join(self.img_folder, options['WALL_IMG'])).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (window['TILESIZE'], window['TILESIZE']))

    def new(self):
        '''
        Initialize game world features and setup for a new game
        '''
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.scrolls = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.play_next_song()

    def get_open_coordinates(self, filename):
        '''
        Load the set of coordinates for dropping collectables
        '''
        return load_occupation_map(filename)

    def run(self):
        '''
        Main game loop
        '''
        while True:
            if self.player.score['parcial'] == 10 or self.elapsed > self.maxTime:
                scores = list(self.player.score.values())[:3]
                self.show_end_screen([i >= 5 for i in scores] == [True, True, True]) # If all score are equal/over 5
                break
            self.dt = self.clock.tick(options['FPS']) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        '''
        Closing the game / Exiting
        '''
        pg.quit()
        sys.exit()

    def update(self):
        '''
        Update portion of the game loop
        '''
        self.all_sprites.update()
        self.camera.update(self.player)

    def drop_scrolls(self):
        '''
        Sequentially spawn the collectables
        '''
        types = ['avlc', 'md', 'calc']
        for i in range(3):
            initWeights = np.random.random(size=len(self.openSet))
            e_w = np.exp(initWeights)
            weights = e_w / e_w.sum() # Softmax function
            choice = (choices(population=self.openSet, weights=list(weights), k=1))[0]
            Scroll(self, choice[1], choice[0], types[i])

    def draw_grid(self):
        '''
        A grid to help the process of developing the game
        '''
        for x in range(0, window['WIDTH'], window['TILESIZE']):
            pg.draw.line(self.screen, window['LIGHT_GREY'], (x, 0), (x, window['HEIGHT']))
        for y in range(0, window['HEIGHT'], window['TILESIZE']):
            pg.draw.line(self.screen, window['LIGHT_GREY'], (0, y), (window['WIDTH'], y))

    def draw(self):
        '''
        '''
        if self.scrollCollected:
                self.drop_scrolls()
                self.scrollCollected = False

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        avlcScore, calcScore, mdScore, partialScore = self.player.score.values()
        avlcCount, calcCount, mdCount = self.player.count.values()
        self.elapsed = time() - self.t0
        string = f"  Faltam {(self.maxTime-self.elapsed)/6:.1f} horas | Nota: {partialScore:.2f}({self.player.scrollCount}) | Álgebra Linear: {avlcScore:.2f}({avlcCount}) | Matemática Discreta: {mdScore:.2f}({mdCount}) | Cálculo: {calcScore:.2f}({calcCount})  "
        text = self.font.render(string, 1, colors['BLACK'], colors['WHITE'])
        self.screen.blit(text, (int((self.screen.get_width() - text.get_width())//2), text.get_height()))
        lastScore = self.player.last
        textColor = colors['RED']
        if lastScore > 0:
            textColor = colors['GREEN']
            lastScore = '+'+str(lastScore)
        text = self.font.render(f' Última Nota: {lastScore} ', 1, textColor, colors['WHITE'])
        self.screen.blit(text, (int((self.screen.get_width() - text.get_width())//2), 700))
        pg.display.flip()

    def events(self):
        '''
        Event catcher
        '''
        for event in pg.event.get():
            # gotta catch 'em all
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                if event.key == pg.K_LCTRL:
                    self.play_next_song()

                # Scroll cheat: fizz
                if self.cheat == 0 and event.key == pg.K_f:
                    self.cheat += 1
                elif self.cheat == 1 and event.key == pg.K_i:
                    self.cheat += 1
                elif self.cheat == 2 and event.key == pg.K_z:
                    self.cheat += 1
                elif self.cheat == 3 and event.key == pg.K_z:
                    self.__scroll_cheat()
                    self.cheat = 0

            if event.type == pg.USEREVENT + 1:  # Song end
                self.play_next_song()

    def play_next_song(self):
        '''
        '''
        self.current_song = 0 if self.current_song == 2 else self.current_song + 1
        pg.mixer.music.load(self.songs[self.current_song])
        pg.mixer.music.play()

    def show_start_screen(self):
        '''
        '''
        startSong = os.path.join(self.game_folder, 'Assets/Audio/menu.mp3')
        pg.mixer.music.load(startSong)
        pg.mixer.music.play(-1)
        while menu.MenuSet().running:
            menu.MenuSet().curr_menu.display_menu()

    def show_end_screen(self, win):
        '''
        '''
        self.screen.fill(colors['DARK_GREY'])
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
            color = (225, 50, 50)
            if win:
                color = (50, 225, 50)
            font = pg.font.Font("C:\Windows\Fonts\Courbd.ttf", 50)
            text = font.render(f'Fim de Jogo', 1, color)
            self.screen.blit(text, (int((self.screen.get_width() - text.get_width())//2), int((self.screen.get_height()-250)//2)))
            font = pg.font.Font("C:\Windows\Fonts\Cour.ttf", 40)
            avlcScore, calcScore, mdScore, partialScore = self.player.score.values()
            avlcCount, calcCount, mdCount = self.player.count.values()
            strings = [f"  Nota: {partialScore:.2f}({self.player.scrollCount})  ",
                        f" Álgebra Linear: {avlcScore:.2f}({avlcCount}) ",
                        f" Matemática Discreta: {mdScore:.2f}({mdCount}) ",
                        f" Cálculo: {calcScore:.2f}({calcCount}) ",
                        f" Tempo gasto: {self.elapsed/6:.2f} horas "]
            height = 0
            for string in strings:
                text = font.render(string, 1, colors['WHITE'])
                self.screen.blit(text, (int((self.screen.get_width() - text.get_width())//2), int((self.screen.get_height()+height)//2)))
                height += text.get_height() + 15
            pg.display.flip()

    def __scroll_cheat(self):
        '''
        Sames as the drop function. To test collection, scores and game ending
        '''
        types = ['avlc', 'md', 'calc']
        for i, coords in enumerate(self.openSet):
            Scroll(self, coords[1], coords[0], types[i%len(types)])


if __name__ == '__main__':
    video()
    g = Game()
    g.show_start_screen()
    g.new()
    g.run()