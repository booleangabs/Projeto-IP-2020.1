import pygame as pg

import sys
import os
from random import choice

from settings import window, options, colors
from sprites import Player, Obstacle, Scroll
from map_tile import TiledMap, Map, Camera, load_occupation_map


class Game:
    '''
    '''
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 30'
        pg.init()
        self.screen = pg.display.set_mode((window['WIDTH'], window['HEIGHT']))
        pg.display.set_caption(window['TITLE'])
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        pg.display.set_icon(window['GAME_LOGO'])
        self.allScrollsCollected = True
        self.current_song = -1
        self.play_next_song()
        self.font = pg.font.Font("C:\Windows\Fonts\Courbd.ttf", 20)
    # Loading Data from folders
    def load_data(self):
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, 'Assets/Images')
        self.audio_folder = os.path.join(self.game_folder, 'Assets/Audio')
        self.songs = [os.path.join(self.audio_folder, f'track-{i}.mp3') for i in range(1, 6)]
        self.map_folder = os.path.join(self.game_folder, 'Tile Map')
        self.map = TiledMap(os.path.join(self.map_folder, 'Map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(os.path.join(self.img_folder, options['PLAYER_IMG'])).convert_alpha()
        self.wall_img = pg.image.load(os.path.join(self.img_folder, options['WALL_IMG'])).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (window['TILESIZE'], window['TILESIZE']))
        
    def new(self):
        # initialize all variables and do all the setup for a new game
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
        self.get_openCoordinates()

    def get_openCoordinates(self):
        #occupationMap = load_occupation_map(os.path.join(self.map_folder, 'scene.npy'))
        pass

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(options['FPS']) / 1000
            self.events()
            self.update()
            self.draw()

    # Closing the game / Exiting
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        if self.allScrollsCollected:
                self.drop_scrolls()
                self.allScrollsCollected = False
        self.all_sprites.update()
        self.camera.update(self.player)
        
    def drop_scrolls(self):
        pass

    # A grid to help the process of developing the game.
    def draw_grid(self):
        for x in range(0, window['WIDTH'], window['TILESIZE']):
            pg.draw.line(self.screen, window['LIGHT_GREY'], (x, 0), (x, window['HEIGHT']))
        for y in range(0, window['HEIGHT'], window['TILESIZE']):
            pg.draw.line(self.screen, window['LIGHT_GREY'], (0, y), (window['WIDTH'], y))

    # To draw things on the Screen
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        string = f"  Nota: {self.player.score['parcial']:.2f} | Álgebra Linear: {self.player.score['avlc']:.2f} | Matemática Discreta: {self.player.score['md']:.2f} | Cálculo: {self.player.score['calc']:.2f}  "
        text = self.font.render(string, 1, colors['BLACK'], colors['WHITE'])
        self.screen.blit(text, (int((self.screen.get_width() - text.get_width())//2), text.get_height()))
        pg.display.flip()


    # Event Catcher
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.USEREVENT + 1: # On song end
                self.play_next_song()

    def play_next_song(self):
        self.current_song = 0 if self.current_song == 2 else self.current_song + 1
        pg.mixer.music.load(self.songs[self.current_song])
        pg.mixer.music.play()

    # For Future Menu Implementation
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
