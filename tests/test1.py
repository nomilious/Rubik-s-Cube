import unittest
from src.annotation import Annotation
import numpy as np
from sklearn.utils import shuffle


class TestStringMethods(unittest.TestCase):
    def startTestRun(self):
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        val = ["W", "R", "Y", "B", "G", "O"]
        for i in range(len(sides)):
            exec(f"self.{sides[i]} = np.array([[val[i]] * 9]).reshape((-1, 3))")

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

            self.assertTrue(self.check_if_equal(annotation), f'Error in testReturningBack() at i={i}')

    def check_if_equal(self, annotation):
        # check if every 2 respective elements of 2 arrays are equal
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        for i in range(len(sides)):
            exec(f"res = np.array_equal(annotation.{sides[i]}, self.{sides[i]})")
            exec(f"assert res is True, f'Error, at i={i}, annotation.{sides[i]} and self.{sides[i]}'")
        return True


if __name__ == '__main__':
    unittest.main()
