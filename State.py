from asyncio.windows_events import NULL

from pygame import SRCALPHA
from Map import Map


class State:
    def __init__(self, x=0, y=0, d=1, v=0) -> None:
        self.x = x
        self.y = y
        self.d = d
        self.v = v

    def _go_on(self, map: Map, v):
        if v == 0:  return self.x, self.y

        if self.d % 2 == 0: # verical direction
            v *= (1-self.d)
            if map._can_move(self.x, self.y, self.y+v, True):
                return self.x, self.y+v
        else: # horizontal direction
            v *= (2-self.d)
            if map._can_move(self.y, self.x, self.x+v, False):
                return self.x+v, self.y
        return -1, -1

    def turn_left(self, map: Map):
        if self.v != 0:
            # print("Can not turn left because v is not 0")
            return NULL
        
        return State(self.x, self.y, (self.d + 1) % 4, self.v)

    def turn_right(self, map: Map):
        if self.v != 0:
            # print("Can not turn right because v is not 0")
            return NULL
        
        return State(self.x, self.y, (self.d - 1) % 4, self.v)

    def speed_up(self, map: Map):
        v = min(self.v+1, map.vmax)
        x, y = self._go_on(map, v)
        if (x, y) == (-1, -1):
            return NULL
        else:
            return State(x, y, self.d, v)

    def slow_down(self, map: Map):
        v = max(self.v-1, 0)
        x, y = self._go_on(map, v)
        if (x, y) == (-1, -1):
            return NULL
        else:
            return State(x, y, self.d, v)

    def no_action(self, map: Map):
        x, y = self._go_on(map, self.v)
        if (x, y) == (-1, -1):
            return NULL
        else:
            return State(x, y, self.d, self.v)

    def friend(self, map: Map):
        tmp = [self.turn_left(map), self.turn_right(map),
            self.slow_down(map), self.speed_up(map)]
        if (self.v != 0):   tmp.append(self.no_action(map))
        
        return list(filter(lambda x: x != NULL, tmp))

    def equals(self, state):
        return (self.x, self.y, self.d, self.v) == (state.x, state.y, state.d, state.v)

if __name__ == "__main__":
    print("State")