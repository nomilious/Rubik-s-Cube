from typing import NewType, Dict
import numpy as np

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


def parser(moves: str, inverse: bool = False) -> [str]:
    return [f"{move}`" if move in "FBLRUD" else move[:-1] for move in moves.split()] if inverse else moves.split()


def get_edge(cube, sides: str) -> Edge:
    cube.do_moves(parser(Edge_to_UF[sides]))

    value = Edge(
        {
            sides[0]: cube.up[2, 1],
            sides[1]: cube.front[0, 1]
        }
    )
    # undo moves
    cube.do_moves(parser(Edge_to_UF[sides], True)[::-1])
    return value


def get_corner(cube, sides: str) -> Corner:
    cube.do_moves(parser(Corners_to_UFR[sides]))

    value = Corner(
        {
            sides[0]: cube.up[-1, -1],
            sides[1]: cube.front[0, -1],
            sides[2]: cube.right[0, 0]
        }
    )
    # undo moves
    cube.do_moves(parser(Corners_to_UFR[sides], True)[::-1])
    return value


def shuffle_cube(cube):
    moves = ['R', "U", "D", "L", "F", "B"]
    for _ in range(np.random.randint(0, 150)):
        move = np.choose(np.random.randint(0, len(moves), size=1), moves)[0]
        dir = np.choose(np.random.randint(0, 2, size=1), [1, -1])[0]
        cube.rotate(Move(move, dir))
