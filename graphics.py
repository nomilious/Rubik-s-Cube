from ursina import *
import math
from Cube import Cube


class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.cube = Cube()

    def input(self, key):
        self.cube.input(key)
        super().input(key)
