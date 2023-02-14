import pickle
import numpy as np
from utils import data_folder

lengths = [4, 8, 16, 32, 64, 128, 256, 512]
repetitions = 10
filename = 'cross_over_times.pickle'
errors_filename = 'cross_over_errors.pickle'

cross_over_times = []
errors = []

# load
# with open(data_folder + filename, "rb") as f:
#     cross_over_times = pickle.load(f)
with open(data_folder + errors_filename, "rb") as f:
    errors = pickle.load(f)

# fix
# for i in range(len(errors)):
#     errors[i] = errors[i] / np.sqrt(repetitions)

# save
# with open(data_folder + filename, "wb") as f:
#     pickle.dump(cross_over_times, f)
with open(data_folder + errors_filename, "wb") as f:
    pickle.dump(errors, f)
