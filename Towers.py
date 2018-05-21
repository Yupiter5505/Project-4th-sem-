import pygame as pg
import SingleNumbers as SN
import random as rnd
import Effects


class Bullet:
    def __init__(self, position: SN.Vector, direction: SN.Vector, damage, effect):
        self.position = position
        self.direction = direction  # Радиус-вектор тайла прибытия
        self.damage = damage
        self.effect = effect

    def update(self, dt):
        self.position = self.position + SN.SingleVelocity * 20 * (self.direction - self.position) * dt


class TypeOfTower:

    def __init__(self, toe, damage, radius, rof, eob=None, aot=None):
        self.toe = toe  # Type Of Enemies
        self.damage = damage
        self.radius = radius
        self.rof = rof  # Rate Of Fire
        self.eob = eob  # Effect Of Bullet
        self.aot = aot  # Ability Of Tower


class Tower:

    def __init__(self, type, x, y, upgrades=None, act=None):
        self.type = type
        self.x = x
        self.y = y
        self.upgrades = upgrades or [0, 0, 0]
        self.act = act or False

    def activate(self):
        self.act = True

    def deactivate(self):
        self.act = False

    def upgrade(self, key, gold):
        if gold >= 10:
            if key == pg.K_KP1:
                self.upgrades[0] += 1
                gold -= 10
            elif key == pg.K_KP2:
                self.upgrades[1] += 1
                gold -= 10
            else:
                self.upgrades[2] += 1
                gold -= 10
            print('Всего золота: ', gold)
            return gold
        print('Недостаточно золота!')
        return gold

    def render_tower(self, canvas):
        if self.type == GroundTower:
            Color = (150, 75, 0)
            pg.draw.rect(canvas, Color, pg.Rect(self.x + 5, self.y + 5, SN.Tile_size - 10, SN.Tile_size - 10))
            if self.act:
                Color = (75, 38, 0)
                pg.draw.rect(canvas, Color, pg.Rect(self.x + 5, self.y + 5, SN.Tile_size - 10, SN.Tile_size - 10), 3)
                pg.draw.circle(canvas, (25, 25, 25), (self.x + SN.Tile_size // 2, self.y + SN.Tile_size // 2),
                               self.type.radius, 2)
        if self.type == FlyTower:
            Color = (102, 0, 255)
            pointlist = [
                (self.x + SN.Tile_size//2, self.y),
                (self.x, self.y + 2*SN.Tile_size//5),
                (self.x + SN.Tile_size//5, self.y + SN.Tile_size),
                (self.x + 4*SN.Tile_size//5, self.y + SN.Tile_size),
                (self.x + SN.Tile_size, self.y + 2*SN.Tile_size//5)
            ]
            pg.draw.polygon(canvas, Color, pointlist)
            if self.act:
                Color = (51, 0, 128)
                pg.draw.polygon(canvas, Color, pointlist, 3)
                pg.draw.circle(canvas, (25, 25, 25), (self.x + SN.Tile_size // 2, self.y + SN.Tile_size // 2),
                               self.type.radius, 2)
        if self.type == EffectTower:
            Color = (124, 146, 124)
            pointlist = [
                (self.x + SN.Tile_size//2, self.y),
                (self.x, self.y + SN.Tile_size),
                (self.x + SN.Tile_size, self.y + SN.Tile_size)
            ]
            pg.draw.polygon(canvas, Color, pointlist)
            if self.act:
                Color = (62, 73, 62)
                pg.draw.polygon(canvas, Color, pointlist, 3)
                pg.draw.circle(canvas, (25, 25, 25), (self.x + SN.Tile_size // 2, self.y + SN.Tile_size // 2),
                               self.type.radius, 2)

    def shoot(self, enemies, bullets):
        pos = SN.Vector(self.x + SN.Tile_size // 2, self.y + SN.Tile_size // 2)
        m = 0
        for i in range(len(enemies)):
            if enemies[i][1][1] > m:
                m = enemies[i][1][1]
        for i in range(len(enemies)):
            dist = (pos * enemies[i][1][0]) ** 0.5
            if dist <= self.type.radius and enemies[i][1][1] == m:
                bullet = Bullet(pos, enemies[i][1][0], self.type.damage, self.type.eob)
                bullets.append(bullet)
        return bullets


SingleDamage = SN.SingleDamage
SingleRadius = SN.SingleRadius
SingleRate = SN.Tile_size
GroundTower = TypeOfTower('Ground', SingleDamage, SingleRadius, SingleRate)
FlyTower = TypeOfTower('Fly', SingleDamage, SingleRadius, SingleRate)
EffectTower = TypeOfTower('All', SingleDamage/2, SingleRadius, SingleRate, rnd.choice(Effects.ListOfEffects))


def BuildTower(gold, key, tile):
    # if type(tile) != Tower:
        if gold >= SN.CoastOfTower:
            if key == pg.K_g:
                tower = Tower(GroundTower, tile.x, tile.y)
            elif key == pg.K_f:
                tower = Tower(FlyTower, tile.x, tile.y)
            elif key == pg.K_e:
                tower = Tower(EffectTower, tile.x, tile.y)
            gold -= SN.CoastOfTower
            print('Всего золота: ', gold)
            tower.activate()
            return tower, gold
        print('Недостаточно золота!')
        return tile, gold

