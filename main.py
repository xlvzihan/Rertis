import pygame
import time
import random
import math
from pygame.locals import *
pygame.init()
myColor = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (255, 255, 0),
           (255, 0, 255), (0, 255, 255), (255, 192, 203), (128, 42, 42)]
screen = pygame.display.set_mode((600, 840))
background = pygame.image.load('./files/bgp.png')
pygame.display.set_caption("Rertis")
screen.blit(background, (0, 0))
pygame.display.update()
manhattan = lambda a, b: abs(a.x - b.x) + abs(a.y - b.y)


class Piece:
    def __init__(self, x, y, clr, movable):
        self.x = x
        self.y = y
        self.color = clr
        self.movable = movable
        self.flag = 0


class Board:
    def __init__(self):
        self.pieces = []
        self.blank = 2.0
        self.next_time = time.time() + self.blank
        self.score = 0
        self.colors = 7
        self.clears = 0
        self.stack = [0, 1]

    def welcome(self):
        homepage = pygame.image.load('./files/welcome.png')
        screen.blit(homepage, (0, 0))
        pygame.display.update()
        while True:
            stack = pygame.event.get()
            for item in stack:
                if item.type == KEYDOWN:
                    if item.key == K_m:
                        self.clears = 3
                        self.stack[0] = random.randint(0, self.colors)
                        self.stack[1] = random.randint(0, self.colors)
                        return
                    elif item.key == K_i:
                        self.clears = 4
                        self.stack[0] = random.randint(0, self.colors)
                        self.stack[1] = random.randint(0, self.colors)
                        return
                elif item.type == QUIT:
                    exit(0)

    def display(self):
        screen.blit(background, (0, 0))
        screen.blit(pygame.font.Font(None, 48).render(str(self.score), True, (0, 0, 0)), (70, 30))
        for item in self.pieces:
            pygame.draw.rect(screen, myColor[item.color], (item.x * 100 + 55, item.y * 100 + 105, 90, 90))
        pygame.draw.rect(screen, myColor[self.stack[1]], (450, 20, 50, 50))
        pygame.display.update()

    def update(self):
        for item in self.pieces:
            if item.movable:
                return True
        for item in self.pieces:
            if item.x == 2 and item.y == 0:
                return False
        self.pieces.append(Piece(2, 0, self.stack[1], 1))
        self.stack.pop(0)
        self.stack.append(random.randint(0, self.colors))
        return True

    def set_blank(self):
        self.blank = 2 * math.exp(-0.005 * self.score)

    def set_next_time(self):
        self.next_time = time.time() + self.blank

    def pause(self):
        paused = pygame.image.load('./files/bgp_paused.png')
        screen.blit(paused, (0, 0))
        screen.blit(pygame.font.Font(None, 48).render(str(self.score), True, (0, 0, 0)), (70, 30))
        pygame.display.update()
        while True:
            waiting = pygame.event.get()
            for item in waiting:
                if item.type == QUIT:
                    exit(0)
                elif item.type == KEYDOWN:
                    if item.key == K_p:
                        self.display()
                        return

    def downwards(self):
        for it in range(len(self.pieces)):
            self.pieces[it].movable = 0
        while True:
            moved = False
            for it in range(len(self.pieces)):
                if self.pieces[it].y == 6:
                    continue
                for another in self.pieces:
                    if (another.x, another.y) == (self.pieces[it].x, self.pieces[it].y + 1):
                        break
                else:
                    moved = True
                    self.pieces[it].y += 1
            if not moved:
                return

    def swap(self):
        for it in range(len(self.pieces)):
            if self.pieces[it].movable == 1:
                self.pieces[it].color = self.stack[1]
                self.stack.reverse()
        self.display()

    def move(self, direction):
        if direction < 2:
            for it in range(len(self.pieces)):
                if self.pieces[it].movable:
                    if self.pieces[it].x + direction not in range(5):
                        return
                    for another in self.pieces:
                        if (another.x, another.y) == (self.pieces[it].x + direction, self.pieces[it].y):
                            return
                    self.pieces[it].x += direction
                    return
        elif direction == 2:
            for it in range(len(self.pieces)):
                if self.pieces[it].movable:
                    if self.pieces[it].y + 1 not in range(7):
                        self.pieces[it].movable = 0
                        bd.clear()
                        return False
                    for another in self.pieces:
                        if (another.x, another.y) == (self.pieces[it].x, self.pieces[it].y + 1):
                            self.pieces[it].movable = 0
                            bd.clear()
                            return False
                    self.pieces[it].y += 1
                    return True
        else:
            self.downwards()
            self.set_next_time()
            self.clear()

    def clear(self):
        bonus = 1
        while True:
            for it in range(len(self.pieces)):
                if self.pieces[it].flag == 0:
                    lst = [it]
                    queue = [it]
                    self.pieces[it].flag = 1
                    number = 1
                    while len(queue):
                        top = queue[0]
                        del queue[0]
                        for another in range(len(self.pieces)):
                            if self.pieces[another].flag == 0 and manhattan(self.pieces[top], self.pieces[another]) == \
                                    1 and self.pieces[another].color == self.pieces[top].color:
                                queue.append(another)
                                lst.append(another)
                                self.pieces[another].flag = 1
                                number += 1
                    if number < self.clears:
                        for iterator in lst:
                            self.pieces[iterator].flag = 0
            count = 0
            for item in self.pieces:
                count += item.flag
            if count:
                self.downwards()
                self.score += bonus * count
                it = 0
                while it < len(self.pieces):
                    if self.pieces[it].flag:
                        del self.pieces[it]
                    else:
                        it += 1
                self.downwards()
                self.display()
                time.sleep(0.5)
                self.next_time += 0.5
                bonus += 1
            else:
                return


bd = Board()
bd.welcome()
while True:
    screen.blit(background, (0, 0))
    eventList = pygame.event.get()
    bd.display()
    for event in eventList:
        bd.display()
        if event.type == QUIT:
            exit(0)
        elif event.type == KEYDOWN:
            if event.key in (K_a, K_LEFT):
                bd.move(-1)
            elif event.key in (K_d, K_RIGHT):
                bd.move(1)
            elif event.key in (K_s, K_DOWN):
                bd.move(2)
            elif event.key in (K_w, K_UP):
                bd.swap()
            elif event.key == K_SPACE:
                bd.move(3)
            elif event.key == K_p:
                bd.pause()
        bd.display()
    if time.time() > bd.next_time:
        bd.move(2)
        bd.set_blank()
        bd.set_next_time()
    bd.display()
    if not bd.update():
        exit(0)
    print(bd.stack)
