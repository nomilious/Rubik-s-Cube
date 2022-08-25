from ursina import *
from src.annotation import Annotation
from src.graphics import Cube
from src.myMath import *


def get_rotation_type(normal, collider_scale):
    ind = [i for i, e in enumerate(normal) if e != 0]
    rest = round(collider_scale[ind[0]] % 1, 2)

    if rest == 2 * Cube.dt:  # is R/L
        return 0
    elif rest == Cube.dt:  # is U/D
        return 1
    return 2  # is F


# IDEA maybe this multiplier type to DELETE because of Cntrl+z BAG of rotation if U/D for UP
def get_multiplier(normal: Vec3, collider_scale: Vec3):
    # additional multilier for rotating our cube, it's needed 'cause of its structure
    flipped = [Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0)]  # back, left, down
    opossite = [Vec3(0, 0, 1), Vec3(1, 0, 0)]  # back, right
    rot_type = get_rotation_type(normal, collider_scale)

    if (rot_type == 0 and normal in opossite) or (rot_type == 2 and normal in flipped):
        return -1
    return 1


# IDEA to recreate ALL colliders on_normalChange()
class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.hist = np.array([])
        self.history_pos = 0

        window.color = color.dark_gray
        window.windowed_size = 0.5
        window.update_aspect_ratio()
        window.late_init()

        self.camera = EditorCamera()
        self.analitic = Annotation()
        self.cube = Cube(1)
        # self.solve = Solve(self.analitic)
        self.action_trigger = True
        self.legal_hist = {'undo': "z up", "redo": "y up", 'next': "mouse1", 'back': 'mouse3'}

    # TODO implement key == 'h' for help panel with all possible move and other info
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

    def movement(self, move: Move):
        self.cube.rotate(move)
        self.analitic.rotate(move)
        # self.analitic.print_cube()
        print(self.hist[:self.history_pos])  # output the histiry taking into account all the undos

        invoke(self.toggle_animation_trigger, delay=0.6 + 0.11)  # we should wait for self.cube.reparent_to_scene()

    # def shuffle(self):
    #     times = randint(1, 200)
    #     hist = np.array(["R", "L", "U", "D", "F", "B"])
    #     for i in range(10):
    #         move = np.random.choice(hist)
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
        elif (not mouse.normal or mouse.normal == Vec3(0, 0, 0)) and key not in [self.legal_hist['undo'], \
                                                                                 self.legal_hist['redo']]:
            return
        self.toggle_animation_trigger()  # stop reading input
        ctrl = 'control'
        # handle input
        if held_keys[ctrl] and key == self.legal_hist['undo']:  # bigger priority
            return self.undo()
        elif held_keys[ctrl] and key == self.legal_hist['redo']:  # bigger priority
            return self.redo()
        elif key == self.legal_hist['next']:  # R, L, F, U, ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = get_multiplier(mouse.normal, hitinfo.entity.scale)
        elif key == self.legal_hist['back']:  # R', L', F', U', ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = -1 * get_multiplier(mouse.normal, hitinfo.entity.scale)
        else:  # quit method
            return self.toggle_animation_trigger()

        move = Move(hitinfo.entity.name, direction)

        # log the move
        self.append_hist(move)
        # do the move
        self.movement(move)

        invoke(self.ab, delay=0.7 + 0.11)  # we should wait for
        # self.cube.reparent_to_scene()

    def ab(self):
        a = [e for e in self.cube.cubes if e.x > 0]
        print(a[1].position, a[1].rotation)

    def append_hist(self, move: Move):
        # cancel redo and change the "history"
        if self.history_pos < len(self.hist):
            self.hist = self.hist[:self.history_pos]

        sign = '' if move.direction == 1 else '`'
        self.hist = np.append(self.hist, [move.face + sign])
        self.history_pos += 1

    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger
