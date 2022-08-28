import copy
from src.utils import *


class Annotation:
    def __init__(self, *args):
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        if not args:
            val = ["W", "R", "Y", "B", "G", "O"]
            for i, side in enumerate(sides):
                setattr(self, side, np.array([[val[i]] * 9]).reshape((-1, 3)))
        else:
            # test
            assert len(args) == 6, "Annotation must have 6 sides"
            for i in range(6):
                assert len(args[i]) == 9, f"Each side must have 9 elements, error on side {i} "
            all_arr = np.concatenate((args[0], args[1], args[2], args[3], args[4], args[5])).tolist()

            check_frequency = lambda arr: all(arr.count(x) == 9 for x in arr)
            assert check_frequency(all_arr), "All sides must have different colors"
            # -------------------------------------------------------------------------
            for i, side_ in enumerate(sides):
                setattr(self, side_, np.array(args[i]).reshape((-1, 3)))

    def rotate(self, move: Move):
        face_rotation_natural = ['L', 'B', 'D']  # rotation is the same as np.rot90

        self.adjacent_rotate(move)
        if move.face not in face_rotation_natural:
            move.direction *= -1
        self.face_rotate(move)

    def adjacent_rotate(self, move: Move):
        match move.face:
            case 'F':
                lst = [copy.deepcopy(self.up[-1, :]), copy.deepcopy(self.left[:, -1][::-1]),
                       copy.deepcopy(self.down[0, :][::-1]), copy.deepcopy(self.right[:, 0])]
                lst = lst[move.direction:] + lst[:move.direction]

                self.up[-1, :] = lst[0]
                self.left[:, -1][::-1] = lst[1]
                self.down[0, :][::-1] = lst[2]
                self.right[:, 0] = lst[3]
            case 'U':
                lst = [copy.deepcopy(self.back[0, :]), copy.deepcopy(self.left[0, :]), copy.deepcopy(self.front[0, :]),
                       copy.deepcopy(self.right[0, :])]
                lst = lst[move.direction:] + lst[:move.direction]

                self.back[0, :], self.left[0, :], self.front[0, :], self.right[0, :] = lst
            case "D":
                lst = [copy.deepcopy(self.back[-1, :]), copy.deepcopy(self.left[-1, :]),
                       copy.deepcopy(self.front[-1, :]),
                       copy.deepcopy(self.right[-1, :])]
                lst = lst[move.direction:] + lst[:move.direction]

                self.back[-1, :], self.left[-1, :], self.front[-1, :], self.right[-1, :] = lst
            case 'R':
                self.y_rotate()
                self.adjacent_rotate(Move('F', move.direction))
                self.y_rotate(3)
            case 'L':
                self.y_rotate(3)
                self.adjacent_rotate(Move('F', -move.direction))
                self.y_rotate()
            case 'B':
                self.y_rotate(2)
                self.adjacent_rotate(Move('F', -move.direction))
                self.y_rotate(2)

    def face_rotate(self, move: Move):
        new_arr = np.rot90(getattr(self, move_to_face[move.face]), move.direction)
        setattr(self, move_to_face[move.face], new_arr)

    def y_rotate(self, times: int = 1):
        for _ in range(times):
            lst = [copy.deepcopy(self.front), copy.deepcopy(self.left), copy.deepcopy(self.back),
                   copy.deepcopy(self.right)]
            lst = lst[-1:] + lst[:-1]
            self.front, self.left, self.back, self.right = lst
            self.face_rotate(Move('D', 1))
            for _ in range(3):
                self.face_rotate(Move('U', 1))

    def do_moves(self, moves: [str]):
        for move_name in moves:
            if move_name == 'y':
                self.y_rotate()
                continue
            self.rotate(Move(move_name))

    def print_cube(self):
        for i in range(9):
            if i % 3 == 0:
                print("\n", end="\t\t\t")
            print(self.up[i // 3][i % 3], end='  ')
        print("\n")

        sides = ['left', 'front', 'right', 'back']
        for i in range(3):
            for side in sides:
                for j in range(3):
                    value = getattr(self, side)[i][j]
                    print(value, end='  ')
                print("", end="\t")
            print()

        for i in range(9):
            if i % 3 == 0:
                print("\n", end="\t\t\t")
            print(self.down[i // 3][i % 3], end='  ')
        print()
