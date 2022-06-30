from ursina import *


app = Ursina()
action_trigger = True
cube_colors = [
    color.blue,  # right
    color.green,   # left
    color.white,    # top
    color.yellow,   # bottom
    color.orange,    # back
    color.red,    # front
]
# create model
size = 1
combine_parent = Entity(enabled=False)
for i in range(3):
    dir = Vec3(0,0,0)
    dir[i] = 1

    e_flipped = Entity(parent=combine_parent, model='plane', origin_y=-.5, color=cube_colors[(i*2)+1])
    e_flipped.look_at(-dir, 'up')

    # e.scale = e_flipped.scale= size

combine_parent.combine()

# place 3x3x3 cubes
cubes = []
for x in range(0, 3*size, size):
    for y in range(0, 3*size, size):
        for z in range(0, 3*size, size):
            e = Entity(
                model=copy(combine_parent.model), 
                position=Vec3(x,y,z) - (Vec3(size,size,size)), 
                texture='white_cube'
            )
            cubes.append(e)


# create_sensors
collider = Entity(model='cube', scale=3*size, collider='box', visible=False)
a= Text(text='')
# get the clicked square
def get_square(position):
    R, L, T, D = 'R', 'L', 'T', 'D' # possition relative to red side
    if (abs(position.z) == 1.5*size):# front and back sides. 
        if position.z > 0:#for 'flipped'
            R, L, T, D = 'L', 'R', 'D', 'T'
        Vec_hor, Vec_ver = position.x, position.y
    elif (abs(position.x) == 1.5*size): # left and right sides. 
        if position.x > 0:#for 'flipped'
            R, L, T, D = 'L', 'R', 'D', 'T'
        Vec_hor, Vec_ver = position.z, position.y
    elif (abs(position.y) == 1.5*size): # top and down sides. 
        if position.y < 0:#for 'flipped'
            R, L, T, D = 'L', 'R', 'D', 'T'
        Vec_hor, Vec_ver = position.x, position.z
    else:
        return 'I don\'t know'

    if abs(Vec_hor) < 0.5*size and abs(Vec_ver) < 0.5*size: #center
        return "center"
    elif abs(Vec_hor) < 1.5*size and abs(Vec_ver) < 0.5*size: # right-left centers
        if Vec_hor > 0:
            return f"{R}center"
        return f"{L}center"
    elif abs(Vec_hor) < 0.5*size and abs(Vec_ver) < 1.5*size: #top-down of centers
        if Vec_ver > 0:
            return f'{T}center'
        return f'{D}center'
    elif abs(Vec_hor) < 1.5*size and abs(Vec_ver) < 1.5*size:# corners
        if Vec_hor > 0 and Vec_ver > 0:
            return f"{T}{R}corner"
        elif Vec_hor < 0 and Vec_ver < 0:
            return f"{D}{L}corner"
        elif Vec_hor > 0 and Vec_ver > 0:
            return f"{D}{R}corner"
        return f"{T}{L}corner"

def input(key):
    if not action_trigger:
        return
    for hitinfo in mouse.collisions:
        collider_name = hitinfo.entity.name
        if key == 'left mouse down':# R, L, F, U
            rotate_side(mouse.normal,mouse.world_point, 1)
        elif key == 'right mouse down':# R', L', F', U'
            rotate_side(mouse.normal,mouse.world_point, -1)

rotation_helper = Entity()
def toggle_animation_trigger():
    '''prohibiting side rotation during rotation animation'''
    global action_trigger
    action_trigger = True

def rotate_side(normal, world_point,direction=1, speed =0.5):
    global cubes, rotation_helper, action_trigger
    action_trigger = False

    square = get_square(world_point) 
    # if normal == Vec3(0,0, -1): # front
    #     if colider_name == 'R':
    #         [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.x > 0]
    #         rotation_helper.animate('rotation_x', 90 * direction, duration=speed)
    #     elif colider_name == 'L':
    #         [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.x < 0]
    #         rotation_helper.animate('rotation_x', 90 * direction, duration=speed)
    #     elif colider_name == 'U':
    #         [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.y > 0]
    #         rotation_helper.animate('rotation_y', 90 * direction, duration=speed)
    #     elif colider_name == 'D':
    #         [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.y < 0]
    #         rotation_helper.animate('rotation_y', 90 * direction, duration=speed)
    
    invoke(reset_rotation_helper, delay=speed+0.11)
    invoke(toggle_animation_trigger, delay=speed+0.11)


def reset_rotation_helper():
    [setattr(e, 'world_parent', scene) for e in cubes]
    rotation_helper.rotation = (0,0,0)
        

EditorCamera()
app.run()