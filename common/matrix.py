from __future__ import annotations


class Matrix(object):

    @staticmethod
    def from_data(data: list[list[float]]):
        result = Matrix(len(data), len(data[0]))
        result.data = data
        result.transpose()
        return result

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data: list[list[float]] = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(0.0)
            self.data.append(row)

    def transpose(self):
        new_data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self[x, y])
            new_data.append(row)

        self.data = new_data
        self.width, self.height = self.height, self.width
        return self

    def normalize(self):
        total = 0.0
        for x in range(self.width):
            for y in range(self.height):
                total += self[x, y]

        for x in range(self.width):
            for y in range(self.height):
                self[x, y] = self[x, y] / total

        return self

    def __getitem__(self, key) -> float:
        return self.data[key[0]][key[1]]

    def __setitem__(self, key, value):
        self.data[key[0]][key[1]] = value

    def copy(self):
        return Matrix.from_data(self.data.copy())

    @property
    def size(self):
        return self.width, self.height
