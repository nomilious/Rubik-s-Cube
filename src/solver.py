import itertools
from src.annotation import Annotation
from src.myMath import *
from src.annotation import *


class Solver:
    def __init__(self, cube):
        self.cube = cube

    def solve_cross(self):
        # successively obtains edges which must be arranged one after the other
        for color in ["R", "G", 'O', "B"]:
            for edge in Edge_to_UF.keys():
                cur_edge = tuple(get_edge(self.cube, edge).values())
                if cur_edge in [(color, "W"), ("W", color)]:
                    # do the needed moves
                    self.cube.do_moves(parser(Edge_to_UF[edge]))

                    # algorithm
                    if get_edge(self.cube, "UF")["U"] == "W":
                        self.cube.do_moves(parser("F F"))
                    else:
                        self.cube.do_moves(parser("R U` R` F"))

                    # shift, to solve next edge
                    self.cube.do_moves(parser("D"))
                    break  # we've solved the needed edge

    def solve_corners(self):
        for colour1, colour2 in [('G', 'R'), ('G', 'O'), ('O', 'B'), ('B', 'R')]:
            for corner in Corners_to_UFR.keys():
                cur_corner = get_corner(self.cube, corner).values()

                if {colour1, colour2, 'W'} == set(cur_corner):
                    self.cube.do_moves(parser(Corners_to_UFR[corner]))

                    # algorithm
                    if get_corner(self.cube, "UFR")['U'] == 'W':
                        moves = "U R U U R` U R U` R`"
                    elif get_corner(self.cube, "UFR")['F'] == 'W':
                        moves = "U R U` R`"
                    else:
                        moves = "R U R`"

                    self.cube.do_moves(parser(moves))
                    self.cube.do_moves(parser("D"))
                    break

    def solve_2layer(self):
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
                cur_edge = tuple(get_edge(self.cube, edge).values())

                if cur_edge in [(colour1, colour2), (colour2, colour1)]:
                    self.cube.do_moves(parser(value))

                    moves = "U R U` R` F R` F` R" if get_edge(self.cube, "UF")[
                                                         'F'] == colour1 else "U U R` F R F` R U R`"

                    self.cube.do_moves(parser(moves))
                    self.cube.y_rotate()
                    break

    def solveTopCross(self):
        for _ in range(4):
            top_layer = [get_edge(self.cube, "UB"), get_edge(self.cube, "UR"),
                         get_edge(self.cube, "UF"), get_edge(self.cube, "UL")]
            type = [face['U'] == 'Y' for face in top_layer]

            if type == [False, False, False, False]:
                moves = "R U U R R F R F` U U R` F R F`"
            elif type == [False, False, True, True]:
                moves = "U F U R U` R` F`"
            elif type == [False, True, False, True]:
                moves = "F R U R` U` F`"
            else:
                moves = "U"
            self.cube.do_moves(parser(moves))

    def solveTopLayer(self):
        alg = "D` R D R` "
        while not self.checkTopSolved():
            if self.cube.back[0, 0] == 'Y':
                self.cube.do_moves(parser(alg * 2))
            elif self.cube.right[0, 2] == 'Y':
                self.cube.do_moves(parser(alg * 4))
            else:
                self.cube.do_moves(parser('U'))

    def solveTopLayerEdge(self):
        alg = "R U R` F` R U R` U` R` F R R U` R` U`"
        for __ in range(4):
            for _ in range(4):
                if [self.cube.front[0, 1], self.cube.right[0, 1]] == [self.cube.front[1, 1], self.cube.right[1, 1]][
                                                                     ::-1]:
                    self.cube.do_moves(parser(alg))
                elif [self.cube.front[0, 1], self.cube.right[0, 1]] == [self.cube.front[1, 1], self.cube.right[1, 1]]:
                    self.cube.y_rotate()
                self.cube.do_moves(parser("U"))
            self.cube.y_rotate()

        # returning to the initial position
        while self.cube.front[0, 1] != self.cube.front[1, 1]:
            self.cube.do_moves(parser("U`"))

    def good_situation(self) -> bool:
        for i, side in enumerate(["front", "right", "back", "left"]):
            if getattr(self.cube, side)[0, 0] == getattr(self.cube, side)[1, 1]:
                for _ in range(i + 1):
                    self.cube.y_rotate()
                return True
        return False

    def solveEdges3Layer(self):
        alg = "R R D` R R D F F R R U` R R U F F"

        while not self.checkSolved():
            self.good_situation()
            self.cube.do_moves(parser(alg))

    def solver(self):
        self.solve_cross()
        self.solve_corners()
        self.solve_2layer()
        self.solveTopCross()
        self.solveTopLayer()
        self.solveTopLayerEdge()
        self.solveEdges3Layer()

    def checkTopSolved(self) -> bool:
        return all(self.cube.up[i][j] == 'Y' for i, j in itertools.product(range(3), range(3)))

    def check2Layer(self) -> bool:
        return not any(
            self.cube.left[1, i] != 'B' or self.cube.right[1, i] != 'G' or self.cube.front[1, i] != 'R' or
            self.cube.back[1, i] != 'O' for i in range(3)
        )

    def checkDownCross(self) -> bool:
        cross = self.cube.down[0, 1] == self.cube.down[1, 0] == self.cube.down[1, 2] == self.cube.down[2, 1]
        adj_edge = [self.cube.left[2, 1], self.cube.front[2, 1], self.cube.right[2, 1], self.cube.back[2, 1]] == \
                   ['B', 'R', 'G', 'O']
        return cross and adj_edge

    def checkTopCross(self) -> bool:
        return self.cube.up[1, 0] == self.cube.up[0, 1] == self.cube.up[1, 2] == self.cube.up[2, 1] == 'Y'

    def checkLayer(self) -> bool:
        return not any(
            self.cube.down[i // 3, i % 3] != 'W' or self.cube.left[-1, i] != 'B' or self.cube.right[-1, i] != 'G' or
            self.cube.front[-1, i] != 'R' or self.cube.back[-1, i] != 'O' for i in range(3)
        )

    def checkSolved(self) -> bool:
        for side in ["front", "right", "back", "left"]:
            for i, j in itertools.product(range(3), range(3)):
                if getattr(self.cube, side)[i, j] != getattr(self.cube, side)[1, 1]:
                    return False
        return True


if __name__ == '__main__':
    for times in range(25000):
        solver = Solver(Annotation())
        shuffle_cube(solver.cube)
        solver.solver()
        a = input()
        assert solver.checkSolved(), "not solved"
        print(f'\r{times} of 25`000', end='')
