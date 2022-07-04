from turtle import position
from ursina import *
import numpy as np

cube_colors = [
    color.green,  # right
    color.blue,  # left
    color.yellow,  # top
    color.white,  # bottom
    color.orange,  # back
    color.red,  # front
]
# сторону можно понять по нормали коллайдера


class Game(Ursina):
    def __init__(self):
        super().__init__()
        self.action_trigger = True
        self.size = 1  # size of squares(width and height)
        window.color = color._16
        self.camera = EditorCamera()
        self.text = Text()
        self.sign = 1
        self.load_game()

    def load_game(self):
        self.create_model()
        self.create_cube()

        self.colliders()  # create_sensors
        self.rotation_helper = Entity()

    def colliders(self):
        dt = 0.1
        self.parent_col = Entity(visible=False)
        create_sensor = lambda n, p, s, c: Entity(
            parent=self.parent_col,
            name=n,
            model="cube",
            position=p,
            scale=s,
            color=c,
            collider="box",
            visible=False,
        )
        L = create_sensor(
            "L",
            (-self.size, 0, 0),
            (self.size, 3 * self.size + 2 * dt, 3 * self.size + 2 * dt),
            color.blue,
        )
        R = create_sensor(
            "R",
            (self.size, 0, 0),
            (self.size, 3 * self.size + 2 * dt, 3 * self.size + 2 * dt),
            color.green,
        )
        F = create_sensor(
            "F",
            (0, 0, -self.size),
            (3 * self.size + 2 * dt, 3 * self.size + dt, self.size),
            color.red,
        )
        BACK_F = create_sensor(
            "B",
            (0, 0, self.size),
            (3 * self.size + 2 * dt, 3 * self.size + dt, self.size),
            color.orange,
        )
        U = create_sensor(
            "U",
            (0, self.size, 0),
            (3 * self.size + dt, self.size, 3 * self.size + dt),
            color.yellow,
        )
        D = create_sensor(
            "D",
            (0, -self.size, 0),
            (3 * self.size + dt, self.size, 3 * self.size + dt),
            color.white,
        )

    def create_model(self):
        self.PARENT = Entity(enabled=False)
        # create cube's sides: right-left, top-down, front-back
        for i in range(3):
            dir = Vec3(0, 0, 0)
            dir[i] = 1
            e = Entity(
                parent=self.PARENT,
                model="plane",
                origin_y=-0.5,
                scale=self.size,
                color=cube_colors[i * 2],
            )

            e_flipped = Entity(
                parent=self.PARENT,
                model="plane",
                origin_y=-0.5,
                scale=self.size,
                color=cube_colors[(i * 2) + 1],
            )
            # rotating according to dir
            e.look_at(dir, "up")
            e_flipped.look_at(-dir, "up")

        self.PARENT.combine()

    def create_cube(self):
        self.cubes = []
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

    def input(self, key):
        print(f"ROTATION:{self.camera.rotation}")
        super().input(key)
        if not self.action_trigger or not mouse.normal:
            return

        for hitinfo in mouse.collisions:
            # TODO direction must depend on normal and key!
            # нучно типа чекать с какой стороны мы нажали !(полярные координаты)
            # Комманда "вверх" зависит не от нормали куда мы нажали, а от поворота камеры
            self.text.text = f"{camera.rotation_directions}"
            if key == "mouse1":  # R, L, F, U
                self.rotate_side(hitinfo.entity.name, mouse.normal, 1)
            elif key == "mouse3":  # R', L', F', U'
                self.rotate_side(hitinfo.entity.name, mouse.normal, -1)
            break

    def toggle_animation_trigger(self):
        """prohibiting side rotation during rotation animation"""
        self.action_trigger = True

    def get_index(self, normal):
        # gets from position the needed ax to rotate around it and the position of the needed cubes
        coords = ["x", "y", "z"]
        a = [(i, int(e)) for i, e in enumerate(normal) if e != 0]
        sign = ">" if a[0][1] > 0 else "<"
        return coords[a[0][0]], sign

    def is_rotation_for_change_dir(self, posx, posy):
        a = abs(round(posx, 0)) % 180
        b = abs(round(posy, 0)) % 180
        dt = 10
        return a + b >= 180 - 2 * dt

    def rotate_side(self, collider, normal, direction=1, speed=0.5):
        self.action_trigger = False
        if self.is_rotation_for_change_dir(camera.rotation_y, camera.rotation_x):
            self.sign = -1
        else:
            self.sign = 1

        # gets the needed ax to rotate around from clicked collider
        for i in self.parent_col.children:
            if i.name == collider:
                coord, sign = self.get_index(i.position)
                # TODO pass direction and handle it
                # TODO change colliders' shapes on_click on every new side
        eval(
            f"[setattr(e, 'world_parent', self.rotation_helper) for e in self.cubes if e.{coord} {sign} 0]",
            {"self": self},
        )
        eval(
            f"self.rotation_helper.animate('rotation_{coord}', 90 * {direction} * {self.sign}, duration={speed})"
        )

        invoke(self.reset_rotation_helper, delay=speed + 0.11)
        invoke(self.toggle_animation_trigger, delay=speed + 0.11)

    def reset_rotation_helper(self):
        [setattr(e, "world_parent", scene) for e in self.cubes]
        self.rotation_helper.rotation = (0, 0, 0)


if __name__ == "__main__":
    game = Game()
    game.run()
