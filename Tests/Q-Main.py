import math
import random
import pygame
import os
from time import sleep


R = 20
W = 500

def reiniciar():
    os.system("killall aplay")
    player.reset((5,5))
    os.system("aplay Sounds/spirited.wav&")



class cube(object):
    rows = R
    w = W

    def __init__(self, start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes =False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            

        numero = random.randint(0,3)

        if numero == 0: #esquerda
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif numero == 1: #direira
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif numero == 2: #cima
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif numero == 3: #baixo
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else:
                c.move(c.dirnx, c.dirny)
            
            if c.dirnx == -1 and c.pos[0] <= 0:
                c.pos = (c.rows - 1, c.pos[1])

            if c.dirnx == 1 and c.pos[0] >= c.rows-1:
                c.pos = (0, c.pos[1])
                
            if c.dirny == 1 and c.pos[1] >= c.rows-1:
                c.pos = (c.pos[0], 0)
                
            if c.dirny == -1 and c.pos[1] <= 0:
                c.pos = (c.pos[0], c.rows-1)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        os.system("aplay Sounds/bounce.wav&")
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    size_btw = w // rows

    x = 0
    y = 0

    for i in range(rows):
        x += size_btw
        y += size_btw

        pygame.draw.line(surface, (70,70,70), (x,0), (x,w))
        pygame.draw.line(surface, (70,70,70), (0,y), (w,y))

def redrawWindow(surface):
    global width, rows, player, snack
    surface.fill((0,120,0))#
    player.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()

def randomSnack(rows, items):
    positions = items.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

def main():
    global width, rows, player, snack
    width = W
    rows = R
    flag = True
    
    window = pygame.display.set_mode((width, width))

    player = snake((255, 0, 0), (5,5))

    snack = cube(randomSnack(rows, player), color=(0, 100, 255))

    clock = pygame.time.Clock()

    os.system("aplay Sounds/spirited.wav&")

    while flag:

        try:

            pygame.time.delay(50) # delay para nao ser tao rapido (quanto menor, mais rapido)
            clock.tick(10) #nao roda com mais de 10 frames por sec (quanto menor, mais lento)

            player.move()

            if player.body[0].pos == snack.pos:
                player.addCube()
                snack = cube(randomSnack(rows, player), color=(0,100,255))

            for x in range(len(player.body)):
                if player.body[x].pos in list(map(lambda z:z.pos, player.body[x+1:])):
                    reiniciar()
                    break
    
            redrawWindow(surface=window)
        
        except:
            os.system("killall aplay")
            break


main()