from typing import NewType, Dict
import numpy as np
from ursina import Vec3, color

# like {Face: color, Face: color,...}
Edge = NewType("Edge", Dict[str, str])
Corner = NewType("Corner", Dict[str, str])


class Move:
    def __init__(self, *args):
        if len(args) == 1:  # str is passed
            self.face = args[0][0]
            self.direction = -1 if args[0][-1] == '`' else 1
        else:
            self.face = args[0]
            self.direction = args[1]


# rotate the needed edge until it's on the top layer on the front face
Edge_to_UF = {
    "UF": "",
    "UL": "U`",
    "UR": "U",
    "UB": "U U",

    "FR": "R U R`",
    "FL": "L U` L`",

    "BL": "L` U` L",
    "BR": "R` U R",

    "DL": "L L U`",
    "DR": "R R U",
    "DB": "B B U U",
    "DF": "F F"
}
move_to_face = {
    'F': 'front',
    'D': 'down',
    'R': 'right',
    'L': 'left',
    'U': 'up',
    'B': 'back',
}
Corners_to_UFR = {
    "DFR": "R U R` U`",
    "DBR": "R` U R U",
    "DFL": "L U` L`",
    "DBL": "L` U L U",

    "UFR": "",
    "URB": "U",
    "ULF": "U`",
    "UBL": "U U",
}

cube_colors = [
    color.green,  # right
    color.blue,  # left
    color.yellow,  # top
    color.white,  # bottom
    color.orange,  # back
    color.red,  # front
]

LEGAL_MOVES = {
    'undo': "z up",
    "redo": "y up",
    "solver": 'a',
    'next': "mouse1",
    'back': 'mouse3'
}

# D stands fro delta
DLEN = 0.02
SPEED = 0.5
DTIME = 0.11


def parser(moves: str, inverse: bool = False) -> [str]:
    return [f"{move}`" if move in "FBLRUD" else move[:-1] for move in moves.split()] if inverse else moves.split()


def getEdges(cube, sides: str) -> Edge:
    cube.doMoves(parser(Edge_to_UF[sides]))

    value = Edge(
        {
            sides[0]: cube.up[2, 1],
            sides[1]: cube.front[0, 1]
        }
    )
    # undo moves
    cube.doMoves(parser(Edge_to_UF[sides], True)[::-1])
    return value


def getCorners(cube, sides: str) -> Corner:
    cube.doMoves(parser(Corners_to_UFR[sides]))

    value = Corner(
        {
            sides[0]: cube.up[-1, -1],
            sides[1]: cube.front[0, -1],
            sides[2]: cube.right[0, 0]
        }
    )
    # undo moves
    cube.doMoves(parser(Corners_to_UFR[sides], True)[::-1])
    return value


def shuffleAnnotation(cube):
    moves = ['R', "U", "D", "L", "F", "B"]
    for _ in range(np.random.randint(0, 150)):
        move = np.choose(np.random.randint(0, len(moves), size=1), moves)[0]
        dir = np.choose(np.random.randint(0, 2, size=1), [1, -1])[0]
        cube.rotate(Move(move, dir))


def getRotationType(normal: Vec3, collider_scale: Vec3) -> int:
    ind = [i for i, e in enumerate(normal) if e != 0]
    rest = round(collider_scale[ind[0]] % 1, 2)

    if rest == 2 * DLEN:  # is R/L
        return 0
    elif rest == DLEN:  # is U/D
        return 1
    return 2  # is F


def getMultiplier(normal: Vec3, collider_scale: Vec3) -> int:
    # additional multiplier for rotating our cube, it's needed 'cause of its structure
    flipped = [Vec3(0, 0, 1), Vec3(-1, 0, 0), Vec3(0, -1, 0)]  # back, left, down
    opposite = [Vec3(0, 0, 1), Vec3(1, 0, 0)]  # back, right
    rot_type = getRotationType(normal, collider_scale)

    if (rot_type == 0 and normal in opposite) or (rot_type == 2 and normal in flipped):
        return -1
    return 1


def getCubiesLocation(normal: Vec3) -> (str, str):
    # gets from position the needed ax to rotate around it and the position of the needed cubes
    coords = ["x", "y", "z"]
    a = [(i, int(e)) for i, e in enumerate(normal) if e != 0]
    sign = ">" if a[0][1] > 0 else "<"

    return coords[a[0][0]], sign
