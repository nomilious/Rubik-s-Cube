from ursina import *
from src.graphics import Cube
from src.annotation import Annotation



def get_rotation_type(collider_scale, normal):
    ind = [i for i, e in enumerate(normal) if e != 0]
    rest = round(collider_scale[ind[0]] % 1, 2)

    if rest == 2 * Cube.dt:  # is R/L
        return 0
    elif rest == Cube.dt:  # is U/D
        return 1
    return 2


def get_multiplier(normal, collider_scale):
    # more clever than using multipliers dict I couldn't invent ...
    # first is R/L, second - D/U, third - F and obviousl R',L',...
    arr = {
        Vec3(0, 0, -1): [1, 1, 1],  # front
        Vec3(0, 0, 1) : [-1, 1, -1],  # back
        Vec3(-1, 0, 0): [1, 1, -1],  # left
        Vec3(1, 0, 0) : [-1, 1, 1],  # right
        Vec3(0, 1, 0) : [1, 1, 1],  # top
        Vec3(0, -1, 0): [1, 1, -1],  # down
    }
    multipliers = arr[normal]

    return multipliers[get_rotation_type(collider_scale, normal)]


# TODO add history of moves
# TODO develop the right and left algorithm
class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.dark_gray
        self.camera = EditorCamera()
        self.analitic = Annotation()
        self.cube = Cube(1)
        self.action_trigger = True

    # IDEA to recreate ALL colliders on_normalChange()
    def input(self, key):
        super().input(key)
        if not self.action_trigger or not mouse.normal:
            return

        self.toggle_animation_trigger()

        for hitinfo in mouse.collisions:
            direction = get_multiplier(mouse.normal, hitinfo.entity.scale)
            if key in ["mouse1", "mouse1 up", "double click"]:  # R, L, F, U
                self.cube.rotate(hitinfo.entity.position, direction)
                self.analitic.rotate_r(hitinfo.entity.name, direction)
            elif key in ["mouse3", "mouse3 up"]:  # R', L', F', U'
                direction *= -1
                self.cube.rotate(hitinfo.entity.position, direction)
                self.analitic.rotate_r(hitinfo.entity.name, direction)
            self.analitic.print_cube()
            break

        invoke(self.toggle_animation_trigger, delay=0.5 + 0.11)

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
