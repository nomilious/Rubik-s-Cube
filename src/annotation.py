import numpy as np
import copy


# IDEA interpret self.back in other way: kind a interpret it as looking in inside this side ? maybe
def get_sides_by_rotation(rot):
    """! relative to self.front
    if R
        down[0,1,2] = back[6,3,0]
        front[2,5,8]= down[0,1,2]
        up[8,7,6] = front[2,5,8]
        back[6,3,0] = up[8,7,6]
    if L
        front[0,3,6]= down[6,7,8]
        down[6,7,8] = back[8,5,2]
        up[2,1,0] = front[0,3,6]
        back[8,5,2] = up[2,1,0]
    if F
        left[2,5,8] = down[6,3,0]
        up[6,3,0] = left[2,5,8]
        right[6,3,0] = up[6,3,0]
        down[6,3,0] = right[6,3,0]
    """
    match rot:
        case "R":
            return 'right', ['front[:,-1]', 'up[-1,:][::-1]', 'back[:,0][::-1]', 'down[0,:]']
        case "L":
            return 'left', ['front[:,0]', 'up[0,:][::-1]', 'back[:,-1][::-1]', 'down[-1,:]']
        case "U":
            return 'up', ['front[0,:]', 'left[0,:]', 'back[0,:]', 'right[0,:]']
        case "D":
            return 'down', ['front[-1,:]', 'left[-1,:]', 'back[-1,:]', 'right[-1,:]']
        case "F":
            return 'front', ['left[:,-1]', 'up[:,0][::-1]', 'right[:,0][::-1]', 'down[:,0][::-1]']
        case "B":
            return 'back', ['left[:,0]', 'up[:,-1][::-1]', 'right[:,-1][::-1]', 'down[:,-1][::-1]']


# TODO add self.Moves to Annotation
class Annotation:
    def __init__(self):
        sides = ['down', 'front', 'up', 'left', 'right', 'back']
        val = ["W", "R", "Y", "B", "G", "O"]
        for i in range(len(sides)):
            exec(f"self.{sides[i]} = np.array([[val[i]] * 9]).reshape((-1, 3))")

    def rotate_r(self, collider, direction = 1):
        main, arr = get_sides_by_rotation(collider)
        flipped = ['down', 'back', 'left']

        arr = arr[::-direction]
        arr1 = arr[1:] + arr[:1]

        direction *= -1 if main in flipped else 1
        exec(f"self.{main} = np.rot90(self.{main}, {-direction})")
        # I'm using temp because the value of first element will be changed when I want to assign it to the last one
        exec(f"temp =copy.deepcopy(self.{arr[0]})")

        for i in range(4 - 1):
            exec(f"self.{arr[i]} = self.{arr1[i]}")
        exec(f"self.{arr[3]}= temp")

    def print_cube(self):
        """
         taking into account the direction of growing of each side, the representation of array is:
         *                 ------------
         *                 | Y8 Y7 Y6 |
         *                 | Y5 Y4 Y3 |
         *                 | Y2 Y1 Y0 |
         *                 ------------
         *   ------------  ------------  ------------  ------------
         *   | O0 O1 O2 |  | B0 B1 B2 |  | R0 R1 O2 |  | G0 G1 G2 |
         *   | O3 O4 O5 |  | B3 B4 B5 |  | R3 R4 O5 |  | G3 G4 G5 |
         *   | O6 O7 O8 |  | B6 B7 B8 |  | R6 R7 O8 |  | G6 G7 G8 |
         *   ------------  ------------  ------------  ------------
         *                 ------------
         *                 | W8 W7 W6 |
         *                 | W5 W4 W3 |
         *                 | W2 W1 W0 |
         *                 ------------
        , AND with rot90 we make them by outputting as shown bellow to functionally be as shown above
         *                 ------------
         *                 | Y0 Y1 Y2 |
         *                 | Y3 Y4 Y5 |
         *                 | Y6 Y7 Y8 |
         *                 ------------
         *   ------------  ------------  ------------  ------------
         *   | O0 O1 O2 |  | B0 B1 B2 |  | R0 R1 O2 |  | G0 G1 G2 |
         *   | O3 O4 O5 |  | B3 B4 B5 |  | R3 R4 O5 |  | G3 G4 G5 |
         *   | O6 O7 O8 |  | B6 B7 B8 |  | R6 R7 O8 |  | G6 G7 G8 |
         *   ------------  ------------  ------------  ------------
         *                 ------------
         *                 | W0 W1 W2 |
         *                 | W3 W4 W5 |
         *                 | W6 W7 W8 |
         *                 ------------
        """

        first = np.rot90(self.up, 2)
        last = np.rot90(self.down, 2)
        for i in range(9):
            if i % 3 == 0:
                print("\n", end="\t\t\t")
            print(first[i // 3][i % 3], end='  ')
        print()
        print()

        sides = ['back', 'left', 'front', 'right']
        for i in range(3):
            for side in sides:
                for j in range(3):
                    exec(f"print(self.{side}[i][j], end='  ')")
                print("", end="\t")
            print()

        for i in range(9):
            if i % 3 == 0:
                print("\n", end="\t\t\t")
            print(last[i // 3][i % 3], end='  ')
        print()
