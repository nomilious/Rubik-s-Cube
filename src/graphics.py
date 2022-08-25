from ursina import *
from src.myMath import Move

cube_colors = [
    color.green,  # right
    color.blue,  # left
    color.yellow,  # top
    color.white,  # bottom
    color.orange,  # back
    color.red,  # front
]


def get_cubes_location(normal: Vec3):
    # gets from position the needed ax to rotate around it and the position of the needed cubes
    coords = ["x", "y", "z"]
    a = [(i, int(e)) for i, e in enumerate(normal) if e != 0]
    sign = ">" if a[0][1] > 0 else "<"

    return coords[a[0][0]], sign


# TODO add constructor Cube(annotation)
class Cube:
    dt = 0.1

    def __init__(self, size: int = 1):
        self.size = size  # size of squares(width and height)

        self.cubes = []
        self.parent_col = Entity(add_to_scene_entities=False)  # colliders' parent
        self.PARENT = Entity(add_to_scene_entities=False)  # needed for creating the model
        self.rotation_helper = Entity(add_to_scene_entities=False)

        self.create_model()
        self.create_cube()
        self.create_sensors()

    def create_sensors(self):
        new_sensor = lambda n, p, s, c, vis = False: Entity(
            parent=self.parent_col,
            name=n, model="cube", texture="white_cube",
            position=p, scale=s,
            color=c, collider="box",
            visible=vis,
        )
        new_sensor(
            "L", (-self.size, 0, 0),
            (self.size, 3 * self.size + 2 * Cube.dt, 3 * self.size + 2 * Cube.dt),
            color.blue,
        )
        new_sensor(
            "R", (self.size, 0, 0),
            (self.size, 3 * self.size + 2 * Cube.dt, 3 * self.size + 2 * Cube.dt),
            color.green,
        )
        new_sensor(
            "F", (0, 0, -self.size),
            (3 * self.size + 2 * Cube.dt, 3 * self.size + Cube.dt, self.size),
            color.red,
        )
        new_sensor(
            "B", (0, 0, self.size),
            (3 * self.size + 2 * Cube.dt, 3 * self.size + Cube.dt, self.size),
            color.orange,
        )
        new_sensor(
            "U", (0, self.size, 0),
            (3 * self.size + Cube.dt, self.size, 3 * self.size + Cube.dt),
            color.yellow,
        )
        new_sensor(
            "D", (0, -self.size, 0),
            (3 * self.size + Cube.dt, self.size, 3 * self.size + Cube.dt),
            color.white,
        )

    def create_model(self):
        # create cube's sides: right-left, top-down, front-back
        for i in range(3):
            dir = Vec3(0, 0, 0)
            dir[i] = 1
            e = Entity(
                parent=self.PARENT, model="plane",
                origin_y=-0.5, scale=self.size,
                color=cube_colors[i * 2],

            )
            e_flipped = Entity(
                parent=self.PARENT, model="plane",
                origin_y=-0.5, scale=self.size,
                color=cube_colors[(i * 2) + 1],
            )
            # rotating according to dir
            e.look_at(dir, "up")
            e_flipped.look_at(-dir, "up")

        self.PARENT.combine()

    def create_cube(self):
        temp = self.size
        for x in range(0, 3 * temp, temp):
            for y in range(0, 3 * temp, temp):
                for z in range(0, 3 * temp, temp):
                    e = Entity(
                        model=copy(self.PARENT.model),
                        texture="white_cube",
                        position=Vec3(x, y, z) - (Vec3(temp, temp, temp)),
                    )
                    self.cubes.append(e)

    def rotate(self, move: Move, speed: int = 0.5):
        # get info about clicked collider
        for i in self.parent_col.children:
            if i.name == move.face:
                coord, sign = get_cubes_location(i.position)
                break

        eval(
            f"[setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.{coord} {sign} 0]",
            {"self": self}
        )  # reparent to self.rotation_helper
        eval(f"self.rotation_helper.animate('rotation_{coord}', 90 * {move.direction}, duration=speed)")

        invoke(self.reparent_to_scene, delay=speed + 0.11)

    def reparent_to_scene(self):
        [setattr(e, "world_parent", scene) for e in self.cubes]
        self.rotation_helper.rotation = (0, 0, 0)
