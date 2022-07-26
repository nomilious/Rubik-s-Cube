from ursina import *
from src.annotation import Annotation
from src.graphics import Cube
import numpy as np
from random import randint
import time


def get_rotation_type(normal, collider_scale):
    ind = [i for i, e in enumerate(normal) if e != 0]
    rest = round(collider_scale[ind[0]] % 1, 2)

    if rest == 2 * Cube.dt:  # is R/L
        return 0
    elif rest == Cube.dt:  # is U/D
        return 1
    return 2  # is F


# BAG of rotation if U/D for UP
def get_multiplier(normal, collider_scale):
    # additional multilier for rotating our cube, it's needed 'cause of its structure
    """"
    arr = {
        Vec3(0, 0, -1): [1, 1, 1],  # front
        Vec3(0, 0, 1) : [-1, 1, -1],  # back
        Vec3(-1, 0, 0): [1, 1, -1],  # left
        Vec3(1, 0, 0) : [-1, 1, 1],  # right
        Vec3(0, 1, 0) : [1, 1, 1],  # top
        Vec3(0, -1, 0): [1, 1, -1],  # down
    }
    """
    flipped = [Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0)]  # back, left, down
    opossite = [Vec3(0, 0, 1), Vec3(1, 0, 0)]  # back, right
    rot_type = get_rotation_type(normal, collider_scale)

    if (rot_type == 0 and normal in opossite) or (rot_type == 2 and normal in flipped):
        return -1
    return 1


# TODO develop the right and left algorithm
# IDEA to recreate ALL colliders on_normalChange()
class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.Moves = np.array([])
        self.history_pos = 0

        window.color = color.dark_gray
        window.windowed_size = 0.3
        window.update_aspect_ratio()
        window.late_init()

        self.camera = EditorCamera()
        self.analitic = Annotation()
        self.cube = Cube(1)
        self.action_trigger = True
        self.legal_moves = {'undo': "z up", "redo": "y up", 'next': "mouse1", 'back': 'mouse3'}

    def undo(self):
        if self.history_pos == 0:
            return self.toggle_animation_trigger()  # action_trigger is True again

        self.history_pos -= 1
        move = self.Moves[self.history_pos]
        direction = -1
        if move[-1] == '`':
            move = move[:1]
            direction = 1

        self.movement(move, direction)

    def redo(self):
        if self.history_pos == len(self.Moves):
            return self.toggle_animation_trigger()

        self.history_pos += 1
        move = self.Moves[self.history_pos - 1]
        direction = 1
        if move[-1] == '`':
            move = move[:1]
            direction = -1

        self.movement(move, direction)

    def movement(self, move, direction):
        self.cube.rotate(move, direction)
        self.analitic.rotate_r(move, direction)
        # self.analitic.print_cube()
        print(self.Moves[:self.history_pos])  # output the histiry taking into account all the undos

        invoke(self.toggle_animation_trigger, delay=0.6 + 0.11)  # we should wait for self.cube.reparent_to_scene()

    # def shuffle(self):
    #     times = randint(1, 200)
    #     moves = np.array(["R", "L", "U", "D", "F", "B"])
    #     for i in range(10):
    #         move = np.random.choice(moves)
    #         dir = np.random.choice([1, -1])
    #         self.append_hist(move, dir)
    #         self.cube.rotate(move, dir, 0.2)
    #         time.sleep(2)
    #         print(i)
    #     self.toggle_animation_trigger()  # stop reading input

    def input(self, key):
        super().input(key)

        # action_trigger stops reading input for some milisec
        if not self.action_trigger:
            return
        elif (not mouse.normal or mouse.normal == Vec3(0, 0, 0)) and key not in [self.legal_moves['undo'], \
                                                                                 self.legal_moves['redo']]:
            return
        self.toggle_animation_trigger()  # stop reading input
        ctrl = 'control'
        # handle input
        if held_keys[ctrl] and key == self.legal_moves['undo']:  # bigger priority
            return self.undo()
        elif held_keys[ctrl] and key == self.legal_moves['redo']:  # bigger priority
            return self.redo()
        elif key == self.legal_moves['next']:  # R, L, F, U, ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = get_multiplier(mouse.normal, hitinfo.entity.scale)
        elif key == self.legal_moves['back']:  # R', L', F', U', ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = -1 * get_multiplier(mouse.normal, hitinfo.entity.scale)
        else:  # quit method
            return self.toggle_animation_trigger()

        # log the move
        self.append_hist(hitinfo.entity.name, direction)
        # do the move
        self.movement(hitinfo.entity.name, direction)

    def append_hist(self, name, direction):
        # cancel redo and change the "history"
        if self.history_pos < len(self.Moves):
            self.Moves = self.Moves[:self.history_pos]

        sign = '' if direction == 1 else '`'
        self.Moves = np.append(self.Moves, [name + sign])
        self.history_pos += 1

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
