import numpy as np
import copy


def print_face(what):
    for i in range(9):
        print(what[i // 3][i % 3], end='\t')
        if (i + 1) % 3 == 0:
            print()
    print()


# IDEA interpret self.back in other way: kind a interpret it as looking in inside of this side ? maybe
def get_sides_by_rotation(rot):
    match rot:
        case "R":
            return 'right', ['front', 'down', 'back', 'up'], ["[:,-1]", "[:,-1]", "[:,0]", "[:,-1]"]
        case "L":
            return 'left', ['front', 'down', 'back', 'up'], ["[:,0]", "[:,0]", "[:,-1]", "[:,0]"]
        case "U":
            return 'up', ['front', 'right', 'back', 'left'], ["[0,:]", "[0,:]", "[0,:]", "[0,:]"]
        case "D":
            return 'down', ['front', 'right', 'back', 'left'], ["[-1,:]", "[-1,:]", "[-1,:]", "[-1,:]"]
        case "F":
            return 'front', ['left', 'down', 'right', 'up'], ["[:,-1]", "[0,:]", "[:,0]", "[-1,:]"]
        case "B":
            return 'back', ['left', 'down', 'right', 'up'], ["[:,-1]", "[-1,:]", "[:,0]", "[0,:]"]


class Annotation:
    def __init__(self):
        self.down = np.array([['W'] * 9]).reshape((-1, 3))
        self.front = np.array([['R'] * 9]).reshape((-1, 3))
        self.up = np.array([['Y'] * 9]).reshape((-1, 3))
        self.left = np.array([['B'] * 9]).reshape((-1, 3))
        self.right = np.array([['G'] * 9]).reshape((-1, 3))
        self.back = np.array([['O'] * 9]).reshape((-1, 3))

    def rotate_r(self, collider, direction = 1):
        main, arr, pos = get_sides_by_rotation(collider)

        arr = arr[::direction]
        pos = pos[::direction]
        arr1 = arr[1:] + arr[:1]
        pos1 = pos[1:] + pos[:1]

        # I'm using temp because the value of first element will be changed when I want to assign it to the last one
        exec(f"self.{main} = np.rot90(self.{main}, {-direction})")
        exec(f"temp =copy.deepcopy(self.{arr[0]}{pos[0]})")

        for i in range(4 - 1):
            exec(f"self.{arr[i]}{pos[i]} = self.{arr1[i]}{pos1[i]}")
        exec(f"self.{arr[3]}{pos[3]} = temp")

    def print_cube(self):
        print_face(self.front)
        print_face(self.down)
        print_face(self.right)
        print_face(self.back)
        print_face(self.left)
        print_face(self.up)

