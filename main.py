import hashlib
import math
import pickle
import random
import sys

import numpy as np
import pygame
import tqdm as tqdm
from pygame import gfxdraw

from Game import Town
from utils import get_color_from_name, get_location_in_game_tree

pygame.init()

game = Town('data2.json')

scale = 80
black = 0, 0, 0
screen = pygame.display.set_mode((scale * 30, scale * 30))
screen.unlock()

with open('characters.pkl', 'rb') as f:
    characters = pickle.load(f)

pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 130)

for t in tqdm.tqdm(range(100000000)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Get agent location nodes
    agent_location_nodes = []
    for character in characters:
        loc_node = get_location_in_game_tree(character, game.tree)
        agent_location_nodes.append(loc_node)

    # Send observations to each agent's memory
    for cidx, charloc in enumerate(zip(characters, agent_location_nodes)):
        character, location = charloc

        # Traversal of game tree from agent's location
        stack = [location]

        while stack:
            current_node = stack.pop()

            if current_node.item:
                character.add_memory_desc(str(current_node.name) + " is " + current_node.status, t)

            for oaidx, loc_node in enumerate(agent_location_nodes):
                if loc_node.description == current_node.description:
                    if cidx != oaidx:  # if there's a different agent that the current agent can see
                        character.add_memory_desc(
                            str(characters[oaidx].name) + " is " + characters[oaidx].current_activity, t)

            for child in reversed(current_node.children):
                stack.append(child)

    screen.fill(black)

    stack = [game.tree]

    while stack:
        node = stack.pop()
        stack.extend(reversed(node.children))

        # Draw the node
        x1, y1 = node.location[0]
        x2, y2 = node.location[1]

        if node.item:  # small object
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

        # Draw characters
        for character in characters:
            text_surface = my_font.render(character.name[0], False, (0, 0, 0))
            screen.blit(text_surface, (character.current_location[0] * scale, character.current_location[1] * scale))

    # pygame.gfxdraw.filled_polygon(screen, ((640, 640), (640, 560), (480, 560), (480, 640)), (255, 0, 0))

    # pygame.gfxdraw.filled_polygon(screen, ((x1, y1), (x1, y2), (x2, y2), (x2, y1)), get_color_from_name(node.color))

    pygame.display.flip()
