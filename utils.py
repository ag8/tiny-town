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
    return np.dot(a, b)/(np.linalg.norm(a) * np.linalg.norm(b))
