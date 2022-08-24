import itertools
from src.annotation import Annotation
from src.analitic_gui import *
from src.annotation import *


def solve_cross():
    # successively obtains edges which must be arranged one after the other
    for color in ["R", "G", 'O', "B"]:
        for edge in Edge_to_UF.keys():
            cur_edge = tuple(get_edge(cube, edge).values())
            if cur_edge in [(color, "W"), ("W", color)]:
                # do the needed moves
                cube.do_moves(parser(Edge_to_UF[edge]))

                # algorithm
                if get_edge(cube, "UF")["U"] == "W":
                    cube.do_moves(parser("F F"))
                else:
                    cube.do_moves(parser("R U` R` F"))

                # shift, to solve next edge
                cube.do_moves(parser("D"))
                break  # we've solved the needed edge


def solve_corners():
    for colour1, colour2 in [('G', 'R'), ('G', 'O'), ('O', 'B'), ('B', 'R')]:
        for corner in Corners_to_UFR.keys():
            cur_corner = get_corner(cube, corner).values()

            if {colour1, colour2, 'W'} == set(cur_corner):
                cube.do_moves(parser(Corners_to_UFR[corner]))

                # algorithm
                if get_corner(cube, "UFR")['U'] == 'W':
                    moves = "U R U U R` U R U` R`"
                elif get_corner(cube, "UFR")['F'] == 'W':
                    moves = "U R U` R`"
                else:
                    moves = "R U R`"

                cube.do_moves(parser(moves))
                cube.do_moves(parser("D"))  # BAG MAYBE

                break


def solve_2layer():
    EDGES = {
        "UF": "",
        "UR": "U",
        "UL": "U`",
        "UB": "U U",

        "FR": "R` F R F` R U R` U`",
        "FL": "L` F` L F L U` L` U",
        "BR": "R` U R B R B` R`",
        "BL": "L` U` L B` L B L`"
    }
    for colour1, colour2 in [('R', 'G'), ('G', 'O'), ('O', 'B'), ('B', 'R')]:
        for edge, value in EDGES.items():
            cur_edge = tuple(get_edge(cube, edge).values())

            if cur_edge in [(colour1, colour2), (colour2, colour1)]:
                cube.do_moves(parser(value))

                moves = "U R U` R` F R` F` R" if get_edge(cube, "UF")['F'] == colour1 else "U U R` F R F` R U R`"

                cube.do_moves(parser(moves))
                cube.y_rotate()

                break


def solveTopCross():
    for _ in range(4):
        top_layer = [get_edge(cube, "UB"), get_edge(cube, "UR"),
                     get_edge(cube, "UF"), get_edge(cube, "UL")]
        type = [face['U'] == 'Y' for face in top_layer]

        if type == [False, False, False, False]:
            moves = "R U U R R F R F` U U R` F R F`"
        elif type == [False, False, True, True]:
            moves = "U F U R U` R` F`"
        elif type == [False, True, False, True]:
            moves = "F R U R` U` F`"
        else:
            moves = "U"
        cube.do_moves(parser(moves))


def check_top_solved(cube):
    return all(cube.up[i][j] == 'Y' for i, j in itertools.product(range(3), range(3)))


# BAG MAYBE I NEED TO DELETE down from flipped and use Ctrl+z, maybe not
def solveTopLayer():
    alg = "D` R D R` "
    while not check_top_solved(cube):
        if cube.back[0, 0] == 'Y':
            cube.do_moves(parser(alg * 2))
        elif cube.right[0, 2] == 'Y':
            cube.do_moves(parser(alg * 4))
        else:
            cube.do_moves(parser('U'))


def solveTopLayerEdge():
    alg = "R U R` F` R U R` U` R` F R R U` R` U`"
    for __ in range(4):
        for _ in range(4):
            if [cube.front[0, 1], cube.right[0, 1]] == [cube.front[1, 1], cube.right[1, 1]][::-1]:
                cube.do_moves(parser(alg))
            elif [cube.front[0, 1], cube.right[0, 1]] == [cube.front[1, 1], cube.right[1, 1]]:
                cube.y_rotate()
            cube.do_moves(parser("U"))
        cube.y_rotate()

    # returning to the initial position
    while cube.front[0, 1] != cube.front[1, 1]:
        cube.do_moves(parser("U`"))


def solved():
    return all(cube.up[i][j] == 'Y' for i, j in itertools.product(range(3), range(3))) and \
           all(cube.down[i][j] == 'W' for i, j in itertools.product(range(3), range(3))) and \
           all(cube.front[i][j] == 'G' for i, j in itertools.product(range(3), range(3))) and \
           all(cube.back[i][j] == 'B' for i, j in itertools.product(range(3), range(3))) and \
           all(cube.left[i][j] == 'R' for i, j in itertools.product(range(3), range(3))) and \
           all(cube.right[i][j] == 'O' for i, j in itertools.product(range(3), range(3)))


def good_situation():
    for i, side in enumerate(["front", "right", "back", "left"]):
        if getattr(cube, side)[0, 0] == getattr(cube, side)[1, 1]:
            for _ in range(i + 1):
                cube.y_rotate()
            return True
    return False


# LAST STEP
def step7():
    alg = "R R D` R R D F F R R U` R R U F F"

    if not good_situation():
        cube.do_moves(parser(alg))
        good_situation()
    cube.print_cube()
    cube.do_moves(parser(alg))
    # FIXME
    if not solved:
        cube.do_moves(parser(alg))


def solver():
    solve_cross()
    solve_corners()
    solve_2layer()
    solveTopCross()
    solveTopLayer()
    solveTopLayerEdge()

    step7()
    cube.print_cube()


if __name__ == '__main__':
    for times in range(25000):
        cube = Annotation()
        shuffle_cube(cube)
        solver()
        a = input("INPUT SOMETHING TO CONTINUE")

        print(f'\r{times} of 25`000', end='')
        assert check_layer(cube), f"cube not solved \n{cube.print_cube()}"
        assert check_top_solved(cube), f"cube not solved \n{cube.print_cube()}"
