from ursina import *

cube_colors = [
    color.green,  # right
    color.blue,  # left
    color.yellow,  # top
    color.white,  # bottom
    color.orange,  # back
    color.red,  # front
]


class Cube():
    def __init__(self, size=1):
        self.size = size  # size of squares(width and height)

        self.cubes = []
        self.parent_col = Entity(add_to_scene_entities=False)
        self.PARENT = Entity(add_to_scene_entities=False)
        self.rotation_helper = Entity(add_to_scene_entities=False)

        self.create_model()
        self.create_cube()
        self.create_sensors()  # create_sensors

    def create_sensors(self):
        dt = 0.1
        create_sensor = lambda n, p, s, c: Entity(
            parent=self.parent_col,
            name=n, model="cube",
            position=p, scale=s,
            color=c, collider="box",
            visible=False,
        )
        L = create_sensor(
            "L", (-self.size, 0, 0),
            (self.size, 3 * self.size + 2 * dt, 3 * self.size + 2 * dt),
            color.blue,
        )
        R = create_sensor(
            "R", (self.size, 0, 0),
            (self.size, 3 * self.size + 2 * dt, 3 * self.size + 2 * dt),
            color.green,
        )
        F = create_sensor(
            "F", (0, 0, -self.size),
            (3 * self.size + 2 * dt, 3 * self.size + dt, self.size),
            color.red,
        )
        BACK_F = create_sensor(
            "B", (0, 0, self.size),
            (3 * self.size + 2 * dt, 3 * self.size + dt, self.size),
            color.orange,
        )
        U = create_sensor(
            "U", (0, self.size, 0),
            (3 * self.size + dt, self.size, 3 * self.size + dt),
            color.yellow,
        )
        D = create_sensor(
            "D", (0, -self.size, 0),
            (3 * self.size + dt, self.size, 3 * self.size + dt),
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

    def get_cubes_location(self, normal):
        # gets from position the needed ax to rotate around it and the position of the needed cubes
        coords = ["x", "y", "z"]
        a = [(i, int(e)) for i, e in enumerate(normal) if e != 0]
        sign = ">" if a[0][1] > 0 else "<"

        return coords[a[0][0]], sign

    def get_rotation_type(self, collider_scale, normal):
        ind = [i for i, e in enumerate(normal) if e != 0]
        rest = round(collider_scale[ind[0]] % self.size, 2)

        if rest == 2 * 0.1:  # is R/L
            return 0
        elif rest == 0.1:  # is U/D
            return 1
        return 2

    def get_multiplier(self, normal, collider_scale):
        # more clever than using multipliers dict I couldn't invent ...
        # first is R/L, second - D/U, third - F and obviousl R',L',...
        arr = {
            Vec3(0, 0, -1): [1, 1, 1],  # front
            Vec3(0, 0, 1): [-1, 1, -1],  # back
            Vec3(-1, 0, 0): [1, 1, -1],  # left
            Vec3(1, 0, 0): [-1, 1, 1],  # right
            Vec3(0, 1, 0): [1, 1, 1],  # top
            Vec3(0, -1, 0): [1, 1, -1],  # down
        }
        multipliers = arr[normal]

        return multipliers[self.get_rotation_type(collider_scale, normal)]

    def rotate_side(self, collider, normal, direction, speed=0.5):
        # get info about clicked collider
        for i in self.parent_col.children:
            if i.name == collider:
                coord, sign = self.get_cubes_location(i.position)
                scale = i.scale
                break

        multiplier = self.get_multiplier(normal, scale)
        eval(f"[setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.{coord} {sign} 0]",
             {"self": self})  # reparent to self.rotation_helper
        eval(f"self.rotation_helper.animate('rotation_{coord}', 90 * {direction}*{multiplier}, duration=speed)")

        invoke(self.reparent_to_scene, delay=speed + 0.11)

    def reparent_to_scene(self):
        [setattr(e, "world_parent", scene) for e in self.cubes]
        self.rotation_helper.rotation = (0, 0, 0)
