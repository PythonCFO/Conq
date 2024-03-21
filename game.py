import pygame as pg

from geo import Country  #Will use World eventually
from player import Player

class Game:
    def __init__(
        self, screen: pg.Surface, clock: pg.time.Clock, window_size: pg.Vector2) -> None:
        self.screen = screen
        self.clock = clock
        self.window_size = window_size
        self.font = pg.font.SysFont(None, 24)
        self.playing = True
        self.phases = ["place_units", "move_units", "attack_country"]
        self.phase_idx = 0
        self.phase = self.phases[self.phase_idx]
        self.phase_timer = pg.time.get_ticks()
        self.world = Country()
        self.player = Player(self.world.countries.get("France"), self.world, (0, 0, 255))

