from ursina import *
from Cube import Cube
from annotation import Annotation


# TODO add history of moves
# TODO develop the right and left algorithm
# TODO array of squares' possition
# TODO высчитывать "direction" в self.input() и переправлять на Annotation

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.dark_gray
        self.camera = EditorCamera()
        self.analitic = Annotation()
        self.cube = Cube(1)
        self.action_trigger = True

    def input(self, key):
        # FIXME doesn't work properly for direction = -1
        # FIXME doesn't work properly for direction = 1 - B white-blue
        super().input(key)
        if not self.action_trigger or not mouse.normal:
            self.analitic.print_cube()
            return
        self.toggle_animation_trigger()

        for hitinfo in mouse.collisions:
            if key in ["mouse1", "mouse1 up", "double click"]:  # R, L, F, U
                self.cube.rotate(hitinfo.entity.name, mouse.normal, 1)
                self.analitic.rotate_r(hitinfo.entity.name, 1)
                break
            elif key in ["mouse3", "mouse3 up"]:  # R', L', F', U'
                self.cube.rotate(hitinfo.entity.name, mouse.normal, -1)
                self.analitic.rotate_r(hitinfo.entity.name, -1)
                break
            elif key == "w":
                self.analitic.print_cube()

        invoke(self.toggle_animation_trigger, delay=0.5 + 0.11)

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
