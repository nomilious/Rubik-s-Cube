import unittest
from src.annotation import Annotation
from src.analitic_gui import *
from src.solver import *
import numpy as np
from sklearn.utils import shuffle


def check_if_equal(annotation):
    # check if every 2 respective elements of 2 arrays are equal
    sides = ['down', 'front', 'up', 'left', 'right', 'back']
    for i in range(len(sides)):
        # res = np.array_equal(annotation.__getattribute__(sides[i]), annotation.__getattribute__(sides[i+1]))
        exec(f"res = np.array_equal(annotation.{sides[i]}, self.{sides[i]})")
        exec(f"assert res is True, f'Error, at i={i}, annotation.{sides[i]} and self.{sides[i]}'")
    return True


class TestStringMethods(unittest.TestCase):
    def startTestRun(self):
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        val = ["W", "R", "Y", "B", "G", "O"]
        for i in range(len(sides)):
            setattr(self, sides[i], np.array([[val[i]] * 9]).reshape((-1, 3)))

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
                    annotation.rotate_r(move[ind], 1)
            for move in reversed(comb_array):
                for ind in range(len(move) - 1, -1, -1):
                    annotation.rotate_r(move[ind], -1)

            self.assertTrue(check_if_equal(annotation), f'Error in testReturningBack() at i={i}')

    def testCross(self):
        for times in range(25000):
            cube = Annotation()
            shuffle_cube(cube)
            solve_cross()
            print(f'\r{times} of 25`000', end='')
            assert check_cross(cube), f"cube not solved \n{cube.print_cube()}"

    def testLayer(self):
        for times in range(25000):
            cube = Annotation()
            shuffle_cube(cube)
            solve_cross()
            solve_corners()

            print(f'\r{times} of 25`000', end='')
            assert check_layer(cube), f"cube not solved \n{cube.print_cube()}"

    def test2Layer(self):
        for times in range(25000):
            cube = Annotation()
            shuffle_cube(cube)
            solve_cross()
            solve_corners()
            solve_2layer()

            print(f'\r{times} of 25`000', end='')
            assert check2Layer(cube), f"cube not solved \n{cube.print_cube()}"

    def testTopCross(self):
        for times in range(25000):
            cube = Annotation()
            shuffle_cube(cube)
            solve_cross()
            solve_corners()
            solve_2layer()
            solveTopCross()

            print(f'\r{times} of 25`000', end='')
            assert checkTopCross(cube), f"cube not solved \n{cube.print_cube()}"

    def testTopSide(self):
        for times in range(25000):
            cube = Annotation()
            shuffle_cube(cube)
            solve_cross()
            solve_corners()
            solve_2layer()
            solveTopCross()
            solveTopLayer()

            print(f'\r{times} of 25`000', end='')
            assert check_top_solved(cube), f"cube not solved \n{cube.print_cube()}"


if __name__ == '__main__':
    unittest.main()
