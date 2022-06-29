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

    e = Entity(
        parent=combine_parent, 
        model='plane', 
        origin_y=-.5, 
        color=cube_colors[i*2]
        )
    e.look_at(dir, 'up')
    print("HEREEEEEEEEEEE ",e.position, e.rotation, e.origin)

    e_flipped = Entity(parent=combine_parent, model='plane', origin_y=-.5, color=cube_colors[(i*2)+1])
    e_flipped.look_at(-dir, 'up')

    print(e.scale)
    e.scale = e_flipped.scale= size
    print("HEEEEEEEEERE",e.scale)

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
# relative to red side(front side)
parent_col = Entity(visible=False)
size+=0.01
L = Entity(parent = parent_col,name = 'L',model='cube', position=(-size, 0, 0), scale=(size, 3*size, 3*size), collider='box', visible=False)
R = Entity(parent = parent_col,name = 'R',model='cube', position=(size, 0, 0), scale=(size, 3*size, 3*size), collider='box', visible=False)
F = Entity(parent = parent_col,name = 'F',model='cube', position=(0,0, -size), scale=(3*size, 3*size, size), collider='box', visible=False)
BACK_F = Entity(parent = parent_col,name = 'BACK_F',model='cube', position=(0,0, size), scale=(3*size, 3*size, size), collider='box', visible=False)
U = Entity(parent = parent_col,name = 'U',model='cube', position=(0,size, 0), scale=(3*size, size, 3*size), collider='box', visible=False)
D = Entity(parent = parent_col,name = 'D',model='cube', position=(0,-size, 0), scale=(3*size, size, 3*size), collider='box', visible=False)
a= Text(text='')

# parent_col.input = input
def input(key):
    # a.text=f'anim_trigger={action_trigger}'
    if action_trigger:
        for hitinfo in mouse.collisions:
            collider_name = hitinfo.entity.name
            if key == 'left mouse down':# R, L, F, U
                rotate_side(mouse.normal,collider_name, 1)
            elif key == 'right mouse down':# R', L', F', U'
                rotate_side(mouse.normal,collider_name, -1)

rotation_helper = Entity()
def toggle_animation_trigger():
    '''prohibiting side rotation during rotation animation'''
    global action_trigger
    action_trigger = True

def rotate_side(normal, colider_name,direction=1, speed =0.5):
    global cubes, rotation_helper, action_trigger
    action_trigger = False
    a.text = colider_name
    if normal == Vec3(0,0, -1): # front
        if colider_name == 'R':
            [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.x > 0]
            rotation_helper.animate('rotation_x', 90 * direction, duration=speed)
        elif colider_name == 'L':
            [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.x < 0]
            rotation_helper.animate('rotation_x', 90 * direction, duration=speed)
        elif colider_name == 'U':
            [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.y > 0]
            rotation_helper.animate('rotation_y', 90 * direction, duration=speed)
        elif colider_name == 'D':
            [setattr(e, 'world_parent', rotation_helper) for e in cubes if e.y < 0]
            rotation_helper.animate('rotation_y', 90 * direction, duration=speed)
    
    invoke(reset_rotation_helper, delay=speed+0.11)
    invoke(toggle_animation_trigger, delay=speed+0.11)


def reset_rotation_helper():
    [setattr(e, 'world_parent', scene) for e in cubes]
    rotation_helper.rotation = (0,0,0)
        

EditorCamera()
app.run()