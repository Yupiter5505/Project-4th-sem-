import pygame as pg
import sys
import random as rnd

import Maps


class Tile:

    def __init__(self, x=None, y=None, d=None, act=None):
        self.x = x or 0
        self.y = y or 0
        self.d = d or Maps.Tile_size
        self.act = act or False

    def activate(self):
        self.act = True

    def deactivate(self):
        self.act = False

    def rect(self):
        return pg.Rect(self.x, self.y, self.d, self.d)

    def render_tile(self, canvas, color):
        Color = (85, 85, 85) if self.act else color
        pg.draw.rect(canvas, Color, self.rect())
        if color == (208, 208, 208):
            pg.draw.rect(canvas, (104, 104, 104), self.rect(), 1)


def create_tile(cortege, tile_size):
    return Tile(cortege[0], cortege[1], tile_size)

def draw_map(Tiles, Map, canvas):
    for i in range(len(Tiles)):
        Tiles[i].render_tile(canvas, Map[i][2])

pg.init()

width = Maps.Map_1_width
height = Maps.Map_1_height

screen = pg.display.set_mode((width, height))
pg.display.set_caption('Tower Defence')
clock = pg.time.Clock()

Tiles = []
for tile in Maps.Map_1:
    Tiles.append(create_tile(tile, Maps.Tile_size))

while True:
    dt = clock.tick(50) / 1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN: #and event.buttons == 1:
            for i in range(len(Maps.Map_1)):
                if Maps.Map_1[i][2] == Maps.Tower_color:
                    sub_x = abs(Maps.Map_1[i][0] - pg.mouse.get_pos()[0])
                    sub_y = abs(Maps.Map_1[i][1] - pg.mouse.get_pos()[1])
                    if sub_x < Maps.Tile_size and sub_y < Maps.Tile_size:
                        Tiles[i].activate()
                        for j in range(len(Tiles)):
                            if Tiles[j].act and j != i:
                                Tiles[j].deactivate()

    screen.fill((255, 255, 255))
    draw_map(Tiles, Maps.Map_1, screen)

    pg.display.flip()
