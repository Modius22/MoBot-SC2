import sc2
from sc2 import run_game, maps, Race, Difficulty, position, Result
from sc2.player import Bot, Computer
from sc2.constants import *
from sc2.data import race_townhalls

import random
from examples.protoss.cannon_rush import CannonRushBot
import cv2
import numpy as np
import time

HEADLESS = False


class MoBot(sc2.BotAI):
    async def on_step(self, iteration: int):
        self.MAX_WORKERS = 50
        #if iteration == 0:
        #    print("Game started")
        #    for worker in self.workers:
        #        await self.do(worker.attack(self.enemy_start_locations[0]))


        await self.distribute_workers()
        await self.build_workers()
        await self.build_overlord()
        await self.expand()
        await self.grow_offensive_buildings()

    async def build_workers(self):
        if len(self.units(DRONE)) < self.MAX_WORKERS and self.units(HATCHERY).amount * 16 > len(self.units(DRONE)):
            #print(len(self.units(DRONE)))
            for larva in self.units(LARVA).ready.noqueue:
                if self.can_afford(DRONE) and not self.already_pending(DRONE):
                    await self.do(larva.train(DRONE))

    async def build_overlord(self):
        if self.supply_left < 5 and not self.already_pending(OVERLORD):
            larvae = self.units(LARVA).ready
            if larvae.exists:
                if self.can_afford(OVERLORD):
                    await self.do(larvae.random.train(OVERLORD))

    async def expand(self):
        if self.units(HATCHERY).amount < 4 and self.can_afford(HATCHERY):
            await self.expand_now()

    async def grow_offensive_buildings(self):
        hatch = self.townhalls.random

        if not (len(self.units(SPAWNINGPOOL)) >= self.already_pending(SPAWNINGPOOL)):
            if self.can_afford(SPAWNINGPOOL) and len(self.units(SPAWNINGPOOL)) < 4:
                await self.build(SPAWNINGPOOL, near=hatch)

        #if self.units(SPAWNINGPOOL).ready.exists:
        #    if not (self.units(LAIR).exists or self.already_pending(LAIR)) and hatch.noqueue:
        #        if self.can_afford(LAIR):
        #            await self.do(hatch.build(LAIR))
#
        #if self.units(LAIR).ready.exists:
        #    builds = [SPIRE, HYDRALISKDEN]
        #    lens = list(map(lambda b: len(self.units(b)), builds))
        #    m = min(lens)
        #    for b in builds:
        #        if not (self.units(b).exists or self.already_pending(b)):
        #            if self.can_afford(b) and len(self.units(b)) <= m and len(self.units(b)) < (
        #                    self.iteration / (self.ITERATIONS_PER_MINUTE / 2)):
        #                await self.build(b, near=hatch)

run_game(maps.get("AbyssalReefLE"), [
    Bot(Race.Zerg, MoBot()),
    Computer(Race.Terran, Difficulty.Hard)
    # Bot(Race.Protoss, CannonRushBot())
], realtime=False)
