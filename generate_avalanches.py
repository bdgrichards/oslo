from model import Model
import pickle
from utils import data_folder


def get_avalanches_data() -> tuple[list[int], list[list[int]]]:
    """
    Returns (lengths, avalanches_list).
    If the data hasn't been saved, it will be generated.
    Generating the data may take some time.
    """
    lengths = [4, 8, 16, 32, 64, 128, 256, 512]
    num_cycles = 100000
    repetitions = 10
    filename = 'avalanches_list.pickle'

    avalanches_list: list[list[int]] = []
    # if saved data, use that, else generate new data
    try:
        # attempt to load the data file
        with open(data_folder + filename, "rb") as f:
            avalanches_list: list[list[int]] = pickle.load(f)
    except:
        # generate the data
        for length in lengths:
            avalanches: list[int] = []

            for _ in range(repetitions):
                model = Model(length)
                # maximum number of grains in steady state is 1/2 * L * 2L = L^2
                for _ in range(length**2):
                    model.cycle()
                # only then count the avalanches
                for _ in range(num_cycles):
                    avalanches.append(model.cycle_with_relax_count())
            avalanches_list.append(avalanches)
            # log progress, since this takes a while
            print(length, 'complete')

        # saving
        with open(data_folder + filename, "wb") as f:
            pickle.dump(avalanches_list, f)

    return (lengths, avalanches_list)
