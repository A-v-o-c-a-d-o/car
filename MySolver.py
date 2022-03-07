from math import sqrt
from time import sleep
from Map import Map
from State import State
import pygame


class MySolver:
    def __init__(self) -> None:
        with open('car.in', 'r') as file:
            lines = [[int(n) for n in line.split()] for line in file.readlines()]

            self.start = State(x= lines[1][0], y= lines[1][1])
            self.goal = (lines[1][2], lines[1][3])
            self.queue = [self.start]
            self.seen = set(self.queue)
            self.path = {self.start: 0}
            # for Q3
            self.visited = set(self.queue)

            self.map = Map(N=lines[0][0], n_walls=lines[0][1], vmax=lines[0][2],
                    fuel_cost=lines[0][3], lines=lines[2:])

    def bfs_result(self, end_state: State):
        ans = [end_state]
        cur_state = end_state
        while not cur_state.equals(self.start):
            cur_state = self.path[cur_state]
            ans.insert(0, cur_state)
        
        return ans

    def was_seen(self, state: State, pre_state: State):
        if (state.x, state.y) == (pre_state.x, pre_state.y):    return False

        for a in self.seen:
            if (a.x, a.y) == (state.x, state.y):    return True
        return False

    def solve_bfs(self):
        while len(self.queue) != 0:
            state = self.queue.pop(0)

            # friend: list of state can go on from this state
            friend = state.friend(self.map)
            
            for a in friend:
                if not self.was_seen(a, state):
                    self.queue.append(a)
                    self.seen.add(a)
                    self.path[a] = state
                if (a.x, a.y) == self.goal:
                    return self.bfs_result(a)

        # print("Can not solve this case")
        return 0

    def was_visited(self, state: State, pre_state: State):
        for a in self.visited:
            if state.equals(a):    return True
        return False

    def go_with_limit_fuel(self, start: State, fuel: int):
        if fuel > 0:
            friend = start.friend(self.map)
            
            for a in friend:
                if not self.was_visited(a, start):
                    self.visited.add(a)
                    self.go_with_limit_fuel(a, fuel= fuel - self.map.fuel_cost - int(sqrt(a.v)))
        

def draw(screen: pygame.Surface, state: State, solver: MySolver, car_img: pygame.Surface):
    # screen.fill((255, 255, 255))
    for i in range(solver.map.N):
        pygame.draw.line(screen, (0, 0, 0), (0, i*120), (600, i*120)) # horizontal
        pygame.draw.line(screen, (0, 0, 0), (i*120, 0), (i*120, 600)) # vertical

    for i in solver.map.h_walls:
        pygame.draw.line(screen, (0, 0, 0), (i[0]*120, i[1]*120), ((i[0]+1)*120, i[1]*120), width= 5)
    for i in solver.map.v_walls:
        pygame.draw.line(screen, (0, 0, 0), (i[0]*120, i[1]*120), (i[0]*120, (i[1]+1)*120), width= 5)

    screen.blit(car_img, (state.x*120, state.y*120))


if __name__ == "__main__":
    pygame.init()  
    screen = pygame.display.set_mode((600, 600))
    screen.fill((255, 255, 255))
    car_img = pygame.image.load('img/car1.jpg')
    # car_img.append(pygame.image.load('img/car1.jpg'))
    # car_img.append(pygame.image.load('img/car1.jpg'))
    # car_img.append(pygame.image.load('img/car1.jpg'))
    FPS = 60
    done = False
    clock = pygame.time.Clock()
    step = 0

    mysolver = MySolver()
    # path = mysolver.solve_bfs()
    mysolver.go_with_limit_fuel(mysolver.start, 10)
    visited = list(mysolver.visited)
    # if path == 0:
    #     done = True
    #     pygame.quit()
    # if path != 0:
    #     for i in path:
    #         print((i.x, i.y))
    # else: print("path = 0")

    while not done:
        """ for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                step += 1
                if step >= len(path):
                    step -= 1
                    done = True
        
        draw(screen= screen, state= path[step], solver= mysolver, car_img= car_img) """


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                step += 1
                if step >= len(visited):
                    step -= 1
                    sleep(5000)
                    done = True
        
        draw(screen= screen, state= visited[step], solver= mysolver, car_img= car_img)


        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()
    exit()