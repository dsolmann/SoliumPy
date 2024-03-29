from common.engine.mechanics.object import Entity, TempEntity
from common.engine.mechanics.object import Item
from common.model.effects import FireEffect


class Ball(Entity):
    id = '150'
    max_speed = 5
    damage_value = 20
    effect = None

    def __init__(self, world, owner):
        super(Ball, self).__init__(world)

        self.owner = owner

    def collide_action(self, lst):
        if not lst:
            return

        target = lst[0]
        if (target.type == 'npc') and (target != self.owner):
            target.hp -= self.damage_value
            if self.effect:
                effect = self.effect(target)
                effect.ticks = 5


class Arrow(TempEntity, Item):
    id = '52'


class FireBall(Ball):
    id = '150:1'
    effect = FireEffect

    def __init__(self, world, owner):
        super(FireBall, self).__init__(world, owner)
