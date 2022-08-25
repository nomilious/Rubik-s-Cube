In ```graphics.py``` is implemented the graphic of cube: created model, created sensors(colliders), created cube and
methods for rotating sides. I've created 6 colliders for all possible rotation

In ```game.py``` is the **main** class, are linked our 2 classes. It's like the *business logic* class.

In ```annonation.py```  is implemented analitic's of this game.

How is implemented rotation? I've created colliders, they have priorities(bigger number - more important)

![img.png](res/img.png)

This is achieved by adding *(to the needed axes)* ```2*Cube.dt``` and ```Cude.dt``` respectively. ```Cube.dt``` is
an arbitrary very small number which is defined in *main.py*

Analiticly the rubik's cube array look like:

- W[0][0] - at corner with G, O, along O
- R[0][0] - at corner with W, G
- Y[0][0] - at corner with B, R, along R
- O[0][0] - at corner with B, W
- B[0][0] - at corner with R, W
- G[0][0] - at corner with O, W

Every side represents a 2D array like [0...3][0...3]

I've used ```action_trigger``` because Ursina is continously reading the input
and if the user clicks when a animation(of rotation) is playing,
then it'll crash

```commandline
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
     if B:
        ...
    """
...
```

Info about print function:

```commandline

     *      My cube analitic representation
     *                 ------------
     *                 | Y0 Y1 Y2 |
     *                 | Y3 Y4 Y5 |
     *                 | Y6 Y7 Y8 |
     *                 ------------
     *   ------------  ------------  ------------  ------------
     *   | B0 B1 B2 |  | R0 R1 R2 |  | G0 G1 G2 |  | O0 O1 O2 |
     *   | B3 B4 B5 |  | R3 R4 R5 |  | G3 G4 G5 |  | O3 O4 O5 |
     *   | B6 B7 B8 |  | R6 R7 R8 |  | G6 G7 G8 |  | O6 O7 O8 |
     *   ------------  ------------  ------------  ------------
     *                 ------------
     *                 | W0 W1 W2 |
     *                 | W3 W4 W5 |
     *                 | W6 W7 W8 |
     *                 ------------
   
```

sides position

```commandline
arr = {
        Vec3(0, 0, -1): [1, 1, 1],  # front
        Vec3(0, 0, 1) : [-1, 1, -1],  # back
        Vec3(-1, 0, 0): [1, 1, -1],  # left
        Vec3(1, 0, 0) : [-1, 1, 1],  # right
        Vec3(0, 1, 0) : [1, 1, 1],  # top
        Vec3(0, -1, 0): [1, 1, -1],  # down
    }

```