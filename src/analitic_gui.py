from typing import NewType, Dict
import numpy as np

# like {Face: color, Face: color,...}
Edge = NewType("Edge", Dict[str, str])
Corner = NewType("Corner", Dict[str, str])

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
    list = ""
    for _ in range(np.random.randint(0, 150)):
        move = np.choose(np.random.randint(0, len(moves), size=1), moves)[0]
        dir = np.choose(np.random.randint(0, 2, size=1), [1, -1])[0]
        cube.new_rotate_r(Move(move, dir))
        # add to a list var move
        list += (move if dir == 1 else f'{move}`') + ' '
    # print(list)


def check2Layer(cube):
    return not any(
        cube.left[1, i] != 'B' or cube.right[1, i] != 'G' or cube.front[1, i] != 'R' or cube.back[1, i] != 'O'
        for i in range(3)
    )


def check_cross(cube):
    cross = cube.down[0, 1] == cube.down[1, 0] == cube.down[1, 2] == cube.down[2, 1]
    adj_edge = [cube.left[2, 1], cube.front[2, 1], cube.right[2, 1], cube.back[2, 1]] == ['B', 'R', 'G', 'O']
    return cross and adj_edge


def checkTopCross(cube):
    return cube.up[1, 0] == cube.up[0, 1] == cube.up[1, 2] == cube.up[2, 1] == 'Y'


def check_layer(cube):
    return not any(
        cube.down[i // 3, i % 3] != 'W' or cube.left[-1, i] != 'B' or cube.right[-1, i] != 'G' or cube.front[-1,
                                                                                                             i] != 'R' or
        cube.back[-1, i] != 'O'
        for i in range(3)
    )


class Move:
    def __init__(self, *args):
        if len(args) == 1:  # str is passed
            self.face = args[0][0]
            self.direction = -1 if args[0][-1] == '`' else 1
        else:
            self.face = args[0]
            self.direction = args[1]
