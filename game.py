from ursina import *
import math
from Cube import Cube


class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.dark_gray
        self.camera = EditorCamera()
        self.cube = Cube(1)
        self.action_trigger = True

    def input(self, key):
        super().input(key)
        if not self.action_trigger or not mouse.normal:
            return
        self.toggle_animation_trigger()
        for hitinfo in mouse.collisions:
            if key in ["mouse1", "mouse1 up", "double click"]:  # R, L, F, U
                self.cube.rotate_side(hitinfo.entity.name, mouse.normal, 1)
                break
            elif key in ["mouse3", "mouse3 up"]:  # R', L', F', U'
                self.cube.rotate_side(hitinfo.entity.name, mouse.normal, -1)
                break
        invoke(self.toggle_animation_trigger, delay=0.5+0.11)

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
