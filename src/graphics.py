from ursina import *
from src.utils import Move, DTIME, DLEN, SPEED
from src.utils import cube_colors, getCubiesLocation


class Cube:
    def __init__(self, size: int = 1):
        self.size = size  # size of squares(width and height)

        self.cubes = []
        self.parentCol = Entity(add_to_scene_entities=False)  # colliders' parent
        self.PARENT = Entity(add_to_scene_entities=False)  # needed for creating the model
        self.rotationHelper = Entity(add_to_scene_entities=False)

        self.createModel()
        self.createCube()
        self.createColliders()

    def createColliders(self):
        new_sensor = lambda n, p, s, c, vis=False: Entity(
            parent=self.parentCol,
            name=n, model="cube", texture="white_cube",
            position=p, scale=s,
            color=c, collider="box",
            visible=vis,
        )
        new_sensor(
            "L", (-self.size, 0, 0),
            (self.size, 3 * self.size + 2 * DLEN, 3 * self.size + 2 * DLEN),
            color.blue,
        )
        new_sensor(
            "R", (self.size, 0, 0),
            (self.size, 3 * self.size + 2 * DLEN, 3 * self.size + 2 * DLEN),
            color.green,
        )
        new_sensor(
            "F", (0, 0, -self.size),
            (3 * self.size + 2 * DLEN, 3 * self.size + DLEN, self.size),
            color.red
        )
        new_sensor(
            "B", (0, 0, self.size),
            (3 * self.size + 2 * DLEN, 3 * self.size + DLEN, self.size),
            color.orange,
        )
        new_sensor(
            "U", (0, self.size, 0),
            (3 * self.size + DLEN, self.size, 3 * self.size + DLEN),
            color.yellow,
        )
        new_sensor(
            "D", (0, -self.size, 0),
            (3 * self.size + DLEN, self.size, 3 * self.size + DLEN),
            color.white,
        )

    def createModel(self):
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

    def createCube(self):
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

    def getCollider(self, n: str) -> Entity:
        for child in self.parentCol.children:
            if child.name == n:
                return child

    def y_rotate(self):
        lst = [deepcopy(self.getCollider(face).position) for face in ['R', 'B', 'L', 'F']]
        lst2 = [deepcopy(self.getCollider(face).scale) for face in ['R', 'B', 'L', 'F']]
        for i, face in enumerate(['F', 'R', 'B', 'L']):
            self.getCollider(face).position = lst[i]
            self.getCollider(face).scale = lst2[i]

    def rotate(self, move: Move, speed: int = SPEED):
        # get info about clicked collider
        coord, sign = getCubiesLocation(self.getCollider(move.face).position)

        eval(
            f"[setattr(e, 'world_parent', self.rotationHelper) for e in self.cubes if e.{coord} {sign} 0]",
            {"self": self}
        )  # reparent to rotationHelper
        eval(f"self.rotationHelper.animate('rotation_{coord}', 90 * {move.direction}, duration=speed)")

        invoke(self.reparentToScene, delay=(speed + DTIME))

    def reparentToScene(self):
        [setattr(e, "world_parent", scene) for e in self.cubes]
        self.rotationHelper.rotation = (0, 0, 0)
