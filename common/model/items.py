from common.engine.mechanics.object import Weapon
from common.model import HealingEffect, PoisonEffect
from common.model.entities import *


class Sword(Weapon):
    id = '50'
    damage_value = 10


class UltimateSword(Sword):
    id = '50:1'
    damage_value = 50


class PoisonSword(Sword):
    id = '50:2'
    damage_value = 20

    def damage(self, npc):
        super(PoisonSword, self).damage(npc)
        effect = PoisonEffect(npc)
        effect.ticks = 5


class HealingSword(Sword):
    id = '50:3'
    damage_value = -1
    action_delay = 5

    def damage(self, npc):
        super(HealingSword, self).damage(npc)
        effect = HealingEffect(npc)
        effect.ticks = 5

    def action(self, *_):
        super(HealingSword, self).action()
        self.owner.hp += 1


class FireStaff(Weapon):
    id = '51'
    damage_value = 5

    def action(self, angle):
        super().action()
        fireball = FireBall(self.world, self.owner)
        fireball.speed.from_polar((FireBall.max_speed, angle))
        fireball.spawn(self.owner.x, self.owner.y)


class Bow(Weapon):
    id = '53'
    damage_value = 1
    max_shoot_force = 10

    def __init__(self, world, owner):
        super().__init__(world, owner)
        self.shooting = False
        self.shoot_force = 0

    def action(self):
        pass  # TODO: aiming


class Coin(Item):
    id = '53'
