from src import game
from src import graphics

if __name__ == '__main__':
    # static field in Cube, the dx collider's size relative to side's
    graphics.Cube.dt = 0.02

    game = game.Game()
    game.run()  # BAG when I click on the cube
