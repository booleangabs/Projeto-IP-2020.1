import pygame as pg
import pytmx

from settings import *


# Updated Collision checker based on a fixed square (Creates something like a hit box)
def collide_hit_rect(sprite_one, sprite_two):
    return sprite_one.hit_rect.colliderect(sprite_two.rect)


# A class that reads the map txt file and builds a map upon it
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)  # Loads the TMX file
        self.width = tm.width * tm.tilewidth  # Gets its dimension
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm  # Assign the data to a variable

    def render(self, surface):  # Rendering the tile map
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):  # Checking for layers
                for x, y, gid, in layer:  # Locating tile coordenates
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):  # Creating the map itself
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


# A class to simulate a camera, which creates a illusion of a following camera.
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # Limiting scrolling to map size
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)
