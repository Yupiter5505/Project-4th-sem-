class Vector:
    def __init__(self,x=None, y=None):
        self.x = x or 0
        self.y = y or 0

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) == Vector:
            return self.x*other.x + self.y*other.y
        else:
            return Vector(self.x*other, self.y*other)

    def __rmul__(self, other):
        if type(other) == Vector:
            return self.x*other.x + self.y*other.y
        else:
            return Vector(self.x*other, self.y*other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def intpair(self):
        v = (int(self.x), int(self.y))
        return v


def found(a, A):
    """Находит элемент a в массиве A и, в случае нахождения, возвращает его количество"""
    n = 0
    for i in A:
        if i == a:
            n += 1
    return n


Tile_size = 50
SingleDamage = 30
SingleRadius = Tile_size*2
SingleRate = Tile_size
DurationOfEffects = 5
CoastOfTower = 30

SingleHealth = 90
SingleVelocity = Tile_size // 4

CoastOfWave = 20
