import pygame as pg
import sys
import random as rnd

import SingleNumbers as SN
import Maps
import Enemies
import Towers


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
    flag = False
    for i in range(len(Tiles)):
        if type(Tiles[i]) == Tile:
            Tiles[i].render_tile(canvas, Map[i][2])
        elif type(Tiles[i]) == Towers.Tower and Tiles[i].act is False:
            Tiles[i].render_tower(canvas)
        else:
            Tows = Tiles[i]
            flag = True
    if flag:
        Tows.render_tower(canvas)


def DestroyTower(gold, tower):
    gold += SN.CoastOfTower // 2 + sum(tower.upgrades)*5
    tile = Tile(tower.x, tower.y)
    tile.activate()
    print('Всего золота: ', gold)
    return tile, gold


pg.init()

width = Maps.Map_1_width
height = Maps.Map_1_height

screen = pg.display.set_mode((width, height))
pg.display.set_caption('Tower Defence')
clock = pg.time.Clock()

Tiles = []
for tile in Maps.Map_1:
    Tiles.append(create_tile(tile, Maps.Tile_size))

T = 0
ZT = 0
NOfWave = 0
NOfEnemy = 0
enemies = []

Gold = 120
towers = []
bullets = []

life = 100
Start = False
GameOver = False
StateOfWave = True

while True:
    dt = clock.tick(50) / 1000.0

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(len(Maps.Map_1)):
                if Maps.Map_1[i][2] == Maps.Tower_color:
                    sub_x = Maps.Map_1[i][0] - pg.mouse.get_pos()[0]
                    sub_y = Maps.Map_1[i][1] - pg.mouse.get_pos()[1]
                    if 0 > sub_x > -SN.Tile_size and 0 > sub_y > -SN.Tile_size:
                        Tiles[i].activate()
                        for j in range(len(Tiles)):
                            if Tiles[j].act and j != i:
                                Tiles[j].deactivate()

        if event.type == pg.KEYDOWN and event.key in [pg.K_g, pg.K_e, pg.K_f]:
            for i in range(len(Maps.Map_1)):
                if Tiles[i].act and type(Tiles[i]) != Towers.Tower:
                    Tiles[i], Gold = Towers.BuildTower(Gold, event.key, Tiles[i])
                    towers.append(Tiles[i])

        if event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
            for i in range(len(Maps.Map_1)):
                if Tiles[i].act:
                    Tiles[i], Gold = DestroyTower(Gold, Tiles[i])

        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            Start = True

        if event.type == pg.KEYDOWN and event.key in [pg.K_KP1, pg.K_KP2, pg.K_KP3]:
            for i in range(len(Tiles)):
                if Tiles[i].act and type(Tiles[i]) != Tile:
                    Gold = Tiles[i].upgrade(event.key, Gold)

    if Start:
        T += dt
        if ZT < int(T):
            ZT = int(T)

        if (ZT % 120 == 0 and ZT != 0) or NOfWave == 0:
            NOfWave += 1
            wave, StateOfWave = Enemies.WaveCreation(NOfWave, Enemies.Types), False
            # print(wave)
            wave.reverse()
            j = 0

        if (ZT % 2 == 0 and ZT != 0) and j != len(wave):
            enemy = wave[j]
            j += 1
            enemies.append(enemy)

        elif len(wave) == 0:
            StateOfWave = True

        # print(len(enemies))

        i = 0
        while i != len(enemies):
            enemies[i] = Enemies.update(enemies[i], dt)
            if enemies[i][1][1] == 19:
                life -= 1
                enemies.pop(i)
                i -= 1
            i += 1

    if GameOver:
        print('Игра окончна!')
        print('Оставшееся золото: ', Gold)
        print('Пройдено волн: ', NOfWave - 1)
        Start = False

    screen.fill((255, 255, 255))
    draw_map(Tiles, Maps.Map_1, screen)
    for i in range(len(enemies)):
        Enemies.render(enemies[i], screen)

    pg.display.flip()
