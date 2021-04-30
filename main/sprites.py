import pygame as pg
import numpy as np

from random import choices
import os

from settings import window, colors, options
from map_tile import collide_hit_rect

vec = pg.math.Vector2  # Implementing vectors as a solution for controlling the player rotation

class Player(pg.sprite.Sprite):
    '''
    The player class: our main character
    '''
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.hit_rect = options['PLAYER_HIT_RECT']
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)  # Player Position / Coordinates
        self.rot = 0
        self.score = {'calc': 0, 'avlc': 0, 'md': 0, 'parcial': 0}
        self.count = {'calc': 0, 'avlc': 0, 'md': 0}
        self.last = 0
        self.scrollCount = 0

    def get_keys(self):
        '''
        Keyboard controls
        '''
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = options['PLAYER_ROT_SPEED']
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -options['PLAYER_ROT_SPEED']
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(options['PLAYER_SPEED'], 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-options['PLAYER_SPEED'] / 2, 0).rotate(-self.rot)

    def wall_collision(self, dir):
        '''
        Checks for collisions and ajusts player position relative to the walls
        '''
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width / 2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height / 2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def scroll_collision(self):
        '''
        Registers player interaction with the collectables
        '''
        hits = pg.sprite.spritecollide(self, self.game.scrolls, False)
        if hits:
            self.last = hits[0].score
            self.score[hits[0].type_] += self.last
            self.score[hits[0].type_] = np.clip(self.score[hits[0].type_], 0, 10)
            self.count[hits[0].type_] += 1
            self.scrollCount += 1
            self.score['parcial'] = sum(list(self.score.values())[:3]) / 3
            self.score['parcial'] = np.clip(self.score['parcial'], 0, 10)
            hits[0].kill()
            if self.scrollCount%3 == 0:
                self.game.scrollCollected = True

    def update(self):
        '''
        '''
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.wall_collision('x')
        self.hit_rect.centery = self.pos.y
        self.wall_collision('y')
        self.rect.center = self.hit_rect.center
        self.scroll_collision()

class Wall(pg.sprite.Sprite):
    '''
    Creates the walls in the game based on the loaded txt map (UNUSED)
    '''
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * window['TILESIZE']
        self.rect.y = y * window['TILESIZE']

class Obstacle(pg.sprite.Sprite):
    '''
    Creates the walls in the game based on the loaded tile-based map
    '''
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Scroll(pg.sprite.Sprite):
    def __init__(self, game, x, y, type_):
        self.groups = game.all_sprites, game.scrolls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(os.path.join(self.game.img_folder, options[f'{type_.upper()}_IMG'])).convert_alpha()
        self.image = pg.transform.scale(self.image, (window['TILESIZE'], window['TILESIZE']))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * window['TILESIZE']
        self.rect.y = y * window['TILESIZE'] 
        self.type_ = type_
        self.score = choices(population=[0.475, 0.75, 1.375, -0.5], weights=[0.5, 0.25, 0.125, 0.125], k=1)[0]
