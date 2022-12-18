import itertools
from src.utils import Edge_to_UF, parser, getEdges, getCorners, Corners_to_UFR
from src.annotation import Annotation


class Solver:
    def __init__(self, cube: Annotation):
        self.cube = cube
        self.Moves = ''

    def solveCross(self):
        # successively obtains edges which must be arranged one after the other
        for color in ["R", "G", 'O', "B"]:
            for edge in Edge_to_UF.keys():
                cur_edge = tuple(getEdges(self.cube, edge).values())
                if cur_edge in [(color, "W"), ("W", color)]:
                    self.cube.doMoves(parser(Edge_to_UF[edge]))  # do the needed moves

                    # algorithm
                    moves = 'F F' if getEdges(self.cube, "UF")["U"] == "W" else ' R U` R` F'
                    self.cube.doMoves(parser(moves))

                    self.cube.doMoves(parser("D"))  # shift, to solve next edge
                    self.Moves += f' {Edge_to_UF[edge]} {moves} D'
                    break  # we've solved the needed edge

    def solveCorners(self):
        for colour1, colour2 in [('G', 'R'), ('G', 'O'), ('O', 'B'), ('B', 'R')]:
            for corner in Corners_to_UFR.keys():
                cur_corner = getCorners(self.cube, corner).values()

                if {colour1, colour2, 'W'} == set(cur_corner):
                    self.cube.doMoves(parser(Corners_to_UFR[corner]))

                    # algorithm
                    if getCorners(self.cube, "UFR")['U'] == 'W':
                        moves = "U R U U R` U R U` R`"
                    elif getCorners(self.cube, "UFR")['F'] == 'W':
                        moves = "U R U` R`"
                    else:
                        moves = "R U R`"

                    self.cube.doMoves(parser(moves))
                    self.cube.doMoves(parser("D"))
                    self.Moves += f' {Corners_to_UFR[corner]} {moves} D'
                    break

    def solve2Layer(self):
        # moves that doesn't break the solved cubies
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
                cur_edge = tuple(getEdges(self.cube, edge).values())
                if cur_edge in [(colour1, colour2), (colour2, colour1)]:
                    self.cube.doMoves(parser(value))
                    moves = "U R U` R` F R` F` R" \
                        if getEdges(self.cube, "UF")['F'] == colour1 \
                        else "U U R` F R F` R U R`"

                    self.cube.doMoves(parser(moves))
                    self.cube.doMoves('y')
                    self.Moves += f' {value} {moves} y'
                    break

    def solveTopCross(self):
        for _ in range(4):
            top_layer = [getEdges(self.cube, "UB"), getEdges(self.cube, "UR"),
                         getEdges(self.cube, "UF"), getEdges(self.cube, "UL")]
            type = [face['U'] == 'Y' for face in top_layer]

            if type == [False, False, False, False]:
                moves = "R U U R R F R F` U U R` F R F`"
            elif type == [False, False, True, True]:
                moves = "U F U R U` R` F`"
            elif type == [False, True, False, True]:
                moves = "F R U R` U` F`"
            else:
                moves = "U"
            self.cube.doMoves(parser(moves))
            self.Moves += f' {moves}'

    def solveTopSide(self):
        alg = "D` R D R` "
        while not self.checkTopSolved():
            if self.cube.back[0, 0] == 'Y':
                moves = alg * 2
            elif self.cube.right[0, 2] == 'Y':
                moves = alg * 4
            else:
                moves = 'U'

            self.cube.doMoves(parser(moves))
            self.Moves += f' {moves}'

    def solveTopLayerEdge(self):
        alg = "R U R` F` R U R` U` R` F R R U` R` U`"
        for __ in range(4):
            for _ in range(4):
                moves = ''
                if [self.cube.front[0, 1], self.cube.right[0, 1]] == [self.cube.front[1, 1], self.cube.right[1, 1]][
                                                                     ::-1]:
                    moves = alg
                    self.cube.doMoves(parser(moves))
                elif [self.cube.front[0, 1], self.cube.right[0, 1]] == [self.cube.front[1, 1], self.cube.right[1, 1]]:
                    moves = 'y'
                    self.cube.doMoves(moves)
                self.cube.doMoves(parser("U"))
                self.Moves += f' {moves} U'
            self.cube.doMoves('y')
            self.Moves += ' y'

        # returning to the initial position
        while self.cube.front[0, 1] != self.cube.front[1, 1]:
            self.cube.doMoves(parser("U`"))
            self.Moves += ' U`'

    def goodSituation(self) -> bool:
        for i, side in enumerate(["front", "right", "back", "left"]):
            if getattr(self.cube, side)[0, 0] == getattr(self.cube, side)[1, 1]:
                for _ in range(i + 1):
                    self.cube.doMoves('y')
                    self.Moves += ' y'
                return True
        return False

    def solveEdges3Layer(self):
        alg = "R R D` R R D F F R R U` R R U F F"
        while not self.checkSolved():
            self.goodSituation()
            self.cube.doMoves(parser(alg))
            self.Moves += f' {alg}'

    def solver(self) -> str:
        if not self.checkDownSide():
            self.solveCross()
        if not self.checkLayer():
            self.solveCorners()
        if not self.check2Layer():
            self.solve2Layer()
        if not self.checkTopCross():
            self.solveTopCross()
        if not self.checkTopSolved():
            self.solveTopSide()
        if not self.checkSolved():
            self.solveTopLayerEdge()
            self.solveEdges3Layer()
        return self.Moves

    def checkTopSolved(self) -> bool:
        return all(self.cube.up[i][j] == 'Y' for i, j in itertools.product(range(3), range(3)))

    def check2Layer(self) -> bool:
        return not any(
            self.cube.left[1, i] != 'B' or self.cube.right[1, i] != 'G' or self.cube.front[1, i] != 'R' or
            self.cube.back[1, i] != 'O' for i in range(3)
        )

    def checkDownSide(self) -> bool:
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
