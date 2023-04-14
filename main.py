import hashlib
import math
import random
import sys

import numpy as np
import pygame
import tqdm as tqdm
from pygame import gfxdraw

from Game import Town
from utils import get_color_from_name

pygame.init()

game = Town('data2.json')

scale = 80
black = 0, 0, 0
screen = pygame.display.set_mode((scale * 30, scale * 30))
screen.unlock()

team_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

for i in tqdm.tqdm(range(100000000)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    stack = [game.tree]

    while stack:
        node = stack.pop()
        stack.extend(reversed(node.children))

        # Draw the node
        x1, y1 = node.location[0]
        x2, y2 = node.location[1]

        if x1 == x2 and y1 == y2:  # small object
            random.seed(int(hashlib.sha1(node.description.encode("utf-8")).hexdigest(), 16) % (10 ** 8))
            x1 += random.random() / 2
            y1 += random.random() / 2

            x2 = x1 + 0.3
            y2 = y1 + 0.3
        else:

            x2 += 1
            y2 += 1

        x1 *= scale
        x2 *= scale
        y1 *= scale
        y2 *= scale

        pygame.gfxdraw.filled_polygon(screen, ((x1, y1), (x1, y2), (x2, y2), (x2, y1)), get_color_from_name(node.color))

    # pygame.gfxdraw.filled_polygon(screen, ((640, 640), (640, 560), (480, 560), (480, 640)), (255, 0, 0))

    # pygame.gfxdraw.filled_polygon(screen, ((x1, y1), (x1, y2), (x2, y2), (x2, y1)), get_color_from_name(node.color))

    pygame.display.flip()
