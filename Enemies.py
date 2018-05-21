import pygame as pg
import random as rnd
import math as m

import SingleNumbers as SN
import Maps


class TypeOfEnemies:

    def __init__(self, color, coast, type, health, velocity, effect=None):
        self.color = color
        self.coast = coast
        self.type = type
        self.health = health
        self.velocity = velocity
        self.effect = effect


class Enemies:

    def __init__(self, type, health=None, velocity=None, OnEffect=None):
        self.type = type
        self.health = health or type.health
        self.velocity = velocity or type.velocity
        self.OnEffect = OnEffect


GeneralColor = (155, 187, 89)
FastColor = (255, 255, 0)
ArmoredColor = (31, 73, 125)
FlyColor = (75, 172, 198)
JetColor = (221, 217, 195)
MagicalColor = (128, 100, 162)
StealthColor = (0, 0, 0)
HealerColor = (255, 255, 102)
BossColor = (247, 150, 70)
CEOColor = (192, 80, 77)

General = TypeOfEnemies(GeneralColor, 1, 'Ground', SN.SingleHealth, SN.SingleVelocity)
Fast = TypeOfEnemies(FastColor, 1, 'Ground', SN.SingleHealth*0.75, SN.SingleVelocity*1.25)
Armored = TypeOfEnemies(ArmoredColor, 1, 'Ground', SN.SingleHealth*1.25, SN.SingleVelocity*0.75)
Fly = TypeOfEnemies(FastColor, 1, 'Fly', SN.SingleHealth, SN.SingleVelocity)
Jet = TypeOfEnemies(JetColor, 1, 'Fly', SN.SingleHealth*0.75, SN.SingleVelocity*1.25)
Magical = TypeOfEnemies(MagicalColor, 0.5, 'Ground', SN.SingleHealth*0.5, SN.SingleVelocity, 'Magical')
Stealth = TypeOfEnemies(StealthColor, 2, 'Fly', SN.SingleHealth*1.5, SN.SingleVelocity, 'Stealth')
Healer = TypeOfEnemies(HealerColor, 4, 'Ground', SN.SingleHealth*2, SN.SingleVelocity, 'Healer')
Boss = TypeOfEnemies(BossColor, 5, 'Ground', SN.SingleHealth*7.5, SN.SingleVelocity)
CEO = TypeOfEnemies(CEOColor, 10, 'Boss', SN.SingleHealth*35, SN.SingleVelocity*0.5)

Types = [General, Fast, Armored, Fly, Jet, Magical, Stealth, Healer, Boss, CEO]
Trace = Maps.Trace


def render(enemy, canvas):
    pg.draw.circle(canvas, enemy[0].type.color, enemy[1][0].intpair(), SN.Tile_size//4)


def update(enemy, dt):
    """пока просто движние"""
    direction = SN.Vector(Trace[enemy[1][1] + 1][0] + SN.Tile_size // 2, Trace[enemy[1][1] + 1][1] + SN.Tile_size // 2)
    direct = direction - enemy[1][0]
    l = (direct * direct) ** 0.5
    direct = direct*(1/l)
    enemy[1][0] = enemy[1][0] + direct*enemy[0].velocity*dt
    if enemy[1][0].x >= direction.x - 5 and enemy[1][0].y >= direction.y - 5:
        enemy[1][1] += 1
    return enemy


def WaveCreation(n, Types):
    """Возвращает список вызываемых врагов"""
    Wave = []
    pos = [SN.Vector(SN.Tile_size*1.5, SN.Tile_size*2.5), 0]
    if n <= 5:
        for i in range(SN.CoastOfWave):
            A = Enemies(Types[0])
            Wave.append([A, pos])
        return Wave

    if n % 25 == 0 and n % 100 != 0:
        B = Enemies(Types[8])
        Wave.append([B, pos])
        Coast = SN.CoastOfWave - Types[8].coast
        for i in range(Coast):
            A = rnd.choice(Types[:5])
            Wave.append([A, pos])
        return Wave

    if n % 100 == 0:
        B = Enemies(Types[9])
        Wave.append([B, pos])
        Coast = SN.CoastOfWave - Types[9]
        for i in range(Coast):
            A = rnd.choice(Types[:5])
            Wave.append([A, pos])
        return Wave

    Coast = SN.CoastOfWave

    if n < 25:
        k = 4
    elif n < 50:
        k = 5
    elif n < 75:
        k = 6
    else:
        k = 7

    while Coast > 0:
        A = Enemies(rnd.choice(Types[:k]))
        if Coast > A.type.coast:
            if A != Types[7]:
                Wave.append([A, pos])
                Coast -= A.type.coast
            elif SN.found(A, Wave) < 2:
                Wave.append([A, pos])
                Coast -= A.type.coast
    return Wave
