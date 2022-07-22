Rubik's Cube game using Python Ursina 3D Engine.
In game the user can:
- Perform R/L/F/D/U rotations
- Perform R'/L'/F'/D'/U' rotations
- Rotate the cube 3d and click different sides

I've used ```action_trigger``` because Ursina is continously reading the input
and if the user clicks when a animation(of rotation) is playing,
then it'll crash

For test: run ```python3 main.py```

In ```graphics.py``` is implemented the graphic of cube: created model, created sensors(colliders), created cube and 
methods for rotating sides. I've created 6 colliders for all possible rotation

In ```game.py``` is the **main** class, are linked our 2 classes. It's like the *business logic* class. 

In ```annonation.py```  is implemented analitic's of this game.

How is implemented rotation? Are created colliders, they have priorities(bigger is more important)
![img.png](media/img.png)

This is achieved by adding *(to the needed axes)* ```2*Cube.dt``` and ```Cude.dt``` respectively. ```Cube.dt``` is 
an arbitrary very small number which is defined in *main.py*