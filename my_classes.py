import numpy as np


class Square:
    def __init__(self, n):
        self.name = n

    def get_name(self):
        return self.name


class Edge:
    def __init__(self, n1, n2):
        self.name1 = Square(n1)
        self.name2 = Square(n2)

    def get_name(self):
        return self.name1.name + self.name2.name


class Corner:
    def __init__(self, n1, n2, n3):
        self.name1 = Square(n1)
        self.name2 = Square(n2)
        self.name3 = Square(n3)

    def get_name(self):
        return self.name1.name + self.name2.name + self.name3.name


class Face:
    def __init__(self, c1, c2, c3, c4, c5):
        """
        colours of face and around the face
            c2  c2  c2
        c5  c1  c1  c1  c3
        c5  c1  c1  c1  c3
        c5  c1  c1  c1  c3
            c4  c4  c4
        """
        self.pos = np.array(
            [Corner(c1, c2, c5), Edge(c1, c2), Corner(c1, c2, c3),
             Edge(c1, c5), Square(c1), Edge(c1, c3),
             Corner(c1, c4, c5), Edge(c1, c4), Corner(c1, c4, c3)
             ]
        ).reshape((-1, 3))

    def print_element(self, ind):
        return self.pos[ind // 3][ind % 3].get_name()
