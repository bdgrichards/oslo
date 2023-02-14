import numpy as np

# folder locations
data_folder = './data/'
figures_folder = './figures/'

# useful functions
def average_different_lengths(a: list[list[int]]) -> list[int]:
    """
    A function to average lists of different lengths.
    All lists are truncated to the shortest length.
    """
    list_lengths = [len(i) for i in a]
    min_length = min(list_lengths)
    for l in a:
        while len(l) > min_length:
            l.pop(-1)
    return list(np.average(a, axis=0))