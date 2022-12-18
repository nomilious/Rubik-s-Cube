from ursina import *
from src.annotation import Annotation
from src.graphics import Cube
from src.utils import *
from src.solver import Solver


class Game(Ursina):
    def __init__(self):
        super().__init__()

        self.camera = EditorCamera()
        self.analitic = Annotation()
        self.cube = Cube(1)

        self.action_trigger = True
        self.hist = np.array([])
        self.history_pos = 0
        self.queueMoves = ''

    def undo(self):
        if self.history_pos == 0:
            return self.toggleAnimationTrigger()  # action_trigger is True again

        self.history_pos -= 1
        move = self.hist[self.history_pos]
        direction = -1
        if move[-1] == '`':
            move = move[:1]
            direction = 1

        self.movement(Move(move, direction))

    def redo(self):
        if self.history_pos == len(self.hist):
            return self.toggleAnimationTrigger()

        self.history_pos += 1
        move = self.hist[self.history_pos - 1]
        direction = 1
        if move[-1] == '`':
            move = move[:1]
            direction = -1

        self.movement(Move(move, direction))

    def movement(self, move: Move, dir: int = 1, speed: float = SPEED):
        if move.face == 'y':
            self.cube.y_rotate()
            self.analitic.y_rotate()
            # we should wait for self.cube.reparent_to_scene()a
            invoke(self.toggleAnimationTrigger, delay=(2 * DTIME + speed))
            return

        self.cube.rotate(Move(move.face, move.direction * dir), speed)
        self.analitic.rotate(move)

        invoke(self.toggleAnimationTrigger,
               delay=(2 * DTIME + speed))  # we should wait for self.cube.reparent_to_scene()

    def solver(self):
        if self.queueMoves == '':
            solver = Solver(deepcopy(self.analitic))
            self.queueMoves = solver.solver()
            self.toggleAnimationTrigger()  # stop reading input
            self.queueMoves = self.queueMoves.split()  # remove leading space
        else:
            if len(self.queueMoves) == 0:  # stop EVERYTHING
                self.queueMoves = ''
                return
            move = Move(self.queueMoves.pop(0))
            self.updateHistory(move)
            dir = 1 if move.face == 'y' else getMultiplier(
                self.cube.getCollider('F').position,
                self.cube.getCollider(move.face).scale
            )
            self.movement(Move(move.face, move.direction), dir, 0.005)

    def input(self, key):
        super().input(key)
        if not self.action_trigger:
            return
        if (not mouse.normal or mouse.normal == Vec3(0, 0, 0)) and key not in list(LEGAL_MOVES.values())[:3]:
            return

        self.toggleAnimationTrigger()  # stop reading input

        # handle input
        if held_keys['a']:
            return self.solver()
            # return self.cube.y_rotate()
        elif held_keys['control'] and key == LEGAL_MOVES['undo']:  # bigger priority
            self.queueMoves = ''
            return self.undo()
        elif held_keys['control'] and key == LEGAL_MOVES['redo']:  # bigger priority
            self.queueMoves = ''
            return self.redo()
        elif key == LEGAL_MOVES['next']:  # R, L, F, U, ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = getMultiplier(mouse.normal, hitinfo.entity.scale)
        elif key == LEGAL_MOVES['back']:  # R', L', F', U', ...
            hitinfo = mouse.collisions[0]  # get first collision, it's the most priority
            direction = -1 * getMultiplier(mouse.normal, hitinfo.entity.scale)
        else:  # quit method
            return self.toggleAnimationTrigger()

        self.queueMoves = ''

        self.updateHistory(Move(hitinfo.entity.name, direction))  # log the move
        self.movement(Move(hitinfo.entity.name, direction))  # do the move

    def updateHistory(self, move: Move):
        # cancel redo and change the "history"
        if self.history_pos < len(self.hist):
            self.hist = self.hist[:self.history_pos]

        sign = '' if move.direction == 1 else '`'
        self.hist = np.append(self.hist, [move.face + sign])
        self.history_pos += 1

    def toggleAnimationTrigger(self):
        self.action_trigger = not self.action_trigger
