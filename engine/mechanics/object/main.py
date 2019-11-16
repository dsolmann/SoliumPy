from pygame.math import Vector2
from pygame.rect import Rect


class Object:
    id = '0'
    type = 'object'
    static = True
    visible = True
    collide = True

    width = 50
    height = 50

    x = 0
    y = 0

    def __init__(self, world, x=0, y=0):
        self.rect = Rect(x, y, self.width, self.height)
        self.world = world

        self.direction = 0
        self.speed = Vector2(0, 0)
        self.chunk = self.world.get_chunk_by_coord(x, y)

    @staticmethod
    def canon_id(i):
        if type(i) == int:
            return str(i)
        if i.count(':') != -1:
            main_id, sub_id = i.split(':')
            if sub_id == 0:
                return main_id
        return i

    def spawn(self, x, y):
        self.rect.center = x, y
        self.world.get_chunk_by_coord(x, y).add(self)