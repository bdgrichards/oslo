# Python 3.10.6
# =========================================================
# Generate steady state pile height data
# =========================================================

import pickle
from model import Model
from utils import data_folder


def get_heights_data() -> tuple[list[int], list[list[int]]]:
    """
    Returns (lengths, height_sequence_list)
    If the data hasn't already been saved, it will be generated. 
    Generating the data may take some time.
    """
    lengths = [4, 8, 16, 32, 64, 128, 256, 512]
    num_cycles = 1000000
    filename = 'pile_heights.pickle'

    height_sequence_list: list[list[int]] = []
    # if saved data, use that, else generate new data
    try:
        # attempt to load the data file
        with open(data_folder + filename, "rb") as f:
            height_sequence_list = pickle.load(f)
    except:
        # generate the data
        for length in lengths:
            height_sequence: list[int] = []
            model = Model(length)
            # maximum number of grains in steady state is 1/2 * L * 2L = L^2
            for _ in range(length**2):
                model.cycle()
            # collect the data
            for _ in range(num_cycles):
                model.cycle()
                height_sequence.append(model.get_pile_height())
            height_sequence_list.append(height_sequence)
            # log progress, since this takes a while
            print(length, 'complete')

        # save the data
        with open(data_folder + filename, "wb") as f:
            pickle.dump(height_sequence_list, f)

    return (lengths, height_sequence_list)
