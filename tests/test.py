import unittest
from src.annotation import Annotation
from src.utils import *
from src.solver import *
import numpy as np
from sklearn.utils import shuffle


class TestStringMethods(unittest.TestCase):
    def startTestRun(self):
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        val = ["W", "R", "Y", "B", "G", "O"]
        for i in range(len(sides)):
            setattr(self, sides[i], np.array([[val[i]] * 9]).reshape((-1, 3)))

    def check_if_equal(self, annotation):
        # check if every 2 respective elements of 2 arrays are equal
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        for i in range(len(sides)):
            res = np.array_equal(getattr(annotation, sides[i]), getattr(self, sides[i]))
            assert res, f'Error, at i={i}, annotation.{sides[i]} and self.{sides[i]}'
        return True

    def testReturningBack(self):
        # test if after any move forward and backward the cube will return to initial position
        self.startTestRun()

        annotation = Annotation()
        divs = [1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72]
        moves = ['R', 'L', 'U', 'D', 'F', 'B']

        for i in range(len(divs)):
            comb_array = shuffle(np.array(np.meshgrid(moves, moves)).T.reshape(-1, divs[i]))
            for move in comb_array:
                for ind in range(len(move)):
                    annotation.rotate(Move(move[ind], 1))
            for move in reversed(comb_array):
                for ind in range(len(move) - 1, -1, -1):
                    annotation.rotate(Move(move[ind], -1))

            assert self.check_if_equal(annotation), f'Error in testReturningBack() at i={i}'

    def testCross(self):
        for times in range(25000):
            solver = Solver(Annotation())
            shuffle_cube(solver.cube)
            solver.solveCross()

            print(f'\rtestCross: {times} of 25`000', end='')
            assert solver.checkDownSide(), f"cube not checkSolved \n{solver.cube.print_cube()}"

    def testLayer(self):
        for times in range(25000):
            solver = Solver(Annotation())
            shuffle_cube(solver.cube)
            solver.solveCross()
            solver.solveCorners()

            print(f'\rtestLayer: {times} of 25`000', end='')
            assert solver.checkDownSide(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkLayer(), f"cube not checkSolved \n{solver.cube.print_cube()}"

    def test2Layer(self):
        for times in range(25000):
            solver = Solver(Annotation())
            shuffle_cube(solver.cube)
            solver.solveCross()
            solver.solveCorners()
            solver.solve2Layer()

            print(f'\rtest2Layer: {times} of 25`000', end='')
            assert solver.check2Layer(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkDownSide(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkLayer(), f"cube not checkSolved \n{solver.cube.print_cube()}"

    def testTopCross(self):
        for times in range(25000):
            solver = Solver(Annotation())
            shuffle_cube(solver.cube)
            solver.solveCross()
            solver.solveCorners()
            solver.solve2Layer()
            solver.solveTopCross()

            print(f'\rtestTopCross: {times} of 25`000', end='')
            assert solver.check2Layer(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkDownSide(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkLayer(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkTopCross(), f"cube not checkSolved \n{solver.cube.print_cube()}"

    def testTopSide(self):
        for times in range(25000):
            solver = Solver(Annotation())
            shuffle_cube(solver.cube)
            solver.solveCross()
            solver.solveCorners()
            solver.solve2Layer()
            solver.solveTopCross()
            solver.solveTopSide()

            print(f'\rtestTopSide: {times} of 25`000', end='')
            assert solver.checkTopSolved(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.check2Layer(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkDownSide(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkLayer(), f"cube not checkSolved \n{solver.cube.print_cube()}"
            assert solver.checkTopCross(), f"cube not checkSolved \n{solver.cube.print_cube()}"

    def testCube(self):
        for times in range(25000):
            solver = Solver(Annotation())
            shuffle_cube(solver.cube)
            solver.solver()

            print(f'\rtestCube: {times} of 25`000', end='')
            assert solver.checkSolved(), f"cube not checkSolved \n{solver.cube.print_cube()}"


if __name__ == '__main__':
    unittest.main()
