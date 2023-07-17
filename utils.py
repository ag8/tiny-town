import numpy as np
from matplotlib import colors


def get_color_from_name(color_name):
    try:
        return tuple([255 * x for x in colors.to_rgba(color_name)])[:3]
    except:
        if color_name == 'light_brown':
            return (204, 153, 102, 1)[:3]
        if color_name == 'dark_brown':
            return (101, 63, 33, 1)[:3]
        if color_name == 'crystal':
            return (64, 224, 208, 1)[:3]
        if color_name == 'dark_red':
            return (139, 0, 0, 1)[:3]
        if color_name == 'light_green':
            return (144, 238, 144)
        print(color_name)


def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_location_in_game_tree(character, tree):
    if tree is None:
        return tree

    stack = [tree]
    potentials = []

    while stack:
        current_node = stack.pop()

        n_c = 0

        for child in reversed(current_node.children):
            # Skip over size-0 objects
            if child.item:
                continue

            # Otherwise, add a child if the agent is still within it
            if child.location[0][0] <= character.current_location[0] <= child.location[1][0] and child.location[0][1] <= \
                    character.current_location[1] <= child.location[1][1]:
                n_c += 1
                stack.append(child)

        if n_c == 0:
            return current_node

    # size = 1000000
    # tightest_node = potentials[0]
    # for node in potentials:
    #     c_size = (node.location[1][0] - node.location[0][0]) * (node.location[1][1] - node.location[0][1])
    #     if c_size < size:
    #         size = c_size
    #         tightest_node = node
    #
    # return tightest_node
