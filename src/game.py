import copy

from ursina import *
from src.annotation import Annotation
from src.graphics import Cube
from src.utils import *
from src.solver import Solver


def get_rotation_type(normal: Vec3, collider_scale: Vec3) -> int:
    ind = [i for i, e in enumerate(normal) if e != 0]
    rest = round(collider_scale[ind[0]] % 1, 2)

    if rest == 2 * CONST_dt:  # is R/L
        return 0
    elif rest == CONST_dt:  # is U/D
        return 1
    return 2  # is F


# IDEA delete all multiplier and use instead self.cube.y_rotate()
# IDEA maybe this multiplier type to DELETE because of Ctrl+z BAG of rotation if U/D for UP
def get_multiplier(normal: Vec3, collider_scale: Vec3) -> int:
    # additional multiplier for rotating our cube, it's needed 'cause of its structure
    flipped = [Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0)]  # back, left, down
    opposite = [Vec3(0, 0, 1), Vec3(1, 0, 0)]  # back, right
    rot_type = get_rotation_type(normal, collider_scale)

    if (rot_type == 0 and normal in opposite) or (rot_type == 2 and normal in flipped):
        return -1
    return 1


# comment
class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.hist = np.array([])
        self.history_pos = 0
        self.queueMoves = ''

        window.color = color.dark_gray
        window.windowed_size = 0.3
        window.update_aspect_ratio()
        window.late_init()

        self.camera = EditorCamera()
        self.analitic = Annotation()
        self.cube = Cube(1)
        # self.solve = Solve(self.analitic)
        self.action_trigger = True
        self.legal_move = {'undo': "z up", "redo": "y up", 'next': "mouse1", 'back': 'mouse3'}

    def undo(self):
        if self.history_pos == 0:
            return self.toggle_animation_trigger()  # action_trigger is True again

        self.history_pos -= 1
        move = self.hist[self.history_pos]
        direction = -1
        if move[-1] == '`':
            move = move[:1]
            direction = 1

        self.movement(Move(move, direction))

    def redo(self):
        if self.history_pos == len(self.hist):
            return self.toggle_animation_trigger()

        self.history_pos += 1
        move = self.hist[self.history_pos - 1]
        direction = 1
        if move[-1] == '`':
            move = move[:1]
            direction = -1

        self.movement(Move(move, direction))

    def movement(self, move: Move, dir: int = 1, speed: int = CONST_speed):
        if move.face == 'y':
            self.cube.y_rotate()
            self.analitic.y_rotate()
            # we should wait for self.cube.reparent_to_scene()a
            invoke(self.toggle_animation_trigger, delay=CONST_dtimeGame)
            return

        self.cube.rotate(Move(move.face, move.direction * dir), speed)
        self.analitic.rotate(move)

        invoke(self.toggle_animation_trigger, delay=CONST_dtimeGame)  # we should wait for self.cube.reparent_to_scene()

    def solver(self):
        if self.queueMoves == '':
            solver = Solver(deepcopy(self.analitic))
            self.queueMoves = solver.solver()
            self.toggle_animation_trigger()  # stop reading input
            self.queueMoves = self.queueMoves.split()  # remove leading space
        else:
            # get str from self.queueMoves until next space
            move = Move(self.queueMoves.pop(0))
            self.append_hist(move)
            dir = 1 if move.face == 'y' else get_multiplier(
                self.cube.get_collider('F').position,
                self.cube.get_collider(move.face).scale
            )
            self.movement(Move(move.face, move.direction), dir, 0.1)

    def input(self, key):
        super().input(key)
        # action_trigger stops reading input for some millisecond
        if not self.action_trigger:
            return
        elif (not mouse.normal or mouse.normal == Vec3(0, 0, 0)) and key not in [self.legal_move['undo'],
                                                                                 self.legal_move['redo'], 'a']:
            return
        self.toggle_animation_trigger()  # stop reading input
        # handle input
        if key == 'a':
            return self.solver()
            # return self.cube.y_rotate()
        elif held_keys['control'] and key == self.legal_move['undo']:  # bigger priority
            self.queueMoves = ''
            return self.undo()
        elif held_keys['control'] and key == self.legal_move['redo']:  # bigger priority
            self.queueMoves = ''
            return self.redo()
        elif key == self.legal_move['next']:  # R, L, F, U, ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = get_multiplier(mouse.normal, hitinfo.entity.scale)

        elif key == self.legal_move['back']:  # R', L', F', U', ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = -1 * get_multiplier(mouse.normal, hitinfo.entity.scale)

        else:  # quit method
            return self.toggle_animation_trigger()

        self.queueMoves = ''

        move = Move(hitinfo.entity.name, direction)

        self.append_hist(move)  # log the move
        self.movement(move)  # do the move

    def append_hist(self, move: Move):
        # cancel redo and change the "history"
        if self.history_pos < len(self.hist):
            self.hist = self.hist[:self.history_pos]

        sign = '' if move.direction == 1 else '`'
        self.hist = np.append(self.hist, [move.face + sign])
        self.history_pos += 1

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
