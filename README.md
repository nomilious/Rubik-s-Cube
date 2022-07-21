Rubik's Cube game using Python Ursina 3D Engine.
In game the user can:
- Perform R/L/F/D/U rotations
- Perform R'/L'/F'/D'/U' rotations
- Rotate the cube 3d and click different sides

I've used ```action_trigger``` because Ursina is continously reading the input
and if the user clicks when a animation(of rotation) is playing,
then it'll crash

For test: run ```python3 main.py```
