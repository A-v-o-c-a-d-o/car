from bisect import bisect_left, bisect_right
from math import sqrt

class Map:
    def __init__(self, N, n_walls, vmax, fuel_cost, lines) -> None:
        self.N = N
        self.n_walls = n_walls
        self.vmax = vmax
        self.fuel_cost = fuel_cost
        self.load_walls(lines=lines)

    def load_walls(self, lines):
        self.h_walls = []
        self.v_walls = []

        for line in lines:
            x0, y0, x1, y1 = line

            if x0 == x1: # horizontal
                self.h_walls.append((x0, max(y0, y1)))
            elif y0 == y1: # vertical
                self.v_walls.append((max(x0, x1), y0))
            else:   print("Error wall:", x0, y0, x1, y1)

        self.h_walls.sort(key= lambda x: x[0])
        self.v_walls.sort(key= lambda x: x[1])

    def _can_move(self, fix, s, e, is_vertical):
        if e < 0 or e >= self.N:
            return False

        s, e = sorted([s, e])
        if is_vertical:
            tmp = filter(lambda x: x[0] == fix, self.h_walls)
            for wall in list(tmp):
                if s < wall[1] <= e:   return False
        else:
            tmp = filter(lambda x: x[1] == fix, self.h_walls)
            for wall in list(tmp):
                if s < wall[0] <= e:   return False
            pass
        return True

if __name__ == "__main__":
    map = Map()
    print(map.h_walls)