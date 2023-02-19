# Python 3.10.6
# =========================================================
# Generate the pile height time series plot
# =========================================================

from utils import data_folder, figures_folder
from model import Model
import pickle
import matplotlib.pyplot as plt

# =========================================================
# parameters
# =========================================================
lengths = [4, 8, 16, 32, 64, 128, 256, 512]
number_cycles = 250000
filename = 'heights.pickle'

# =========================================================
# get data
# =========================================================
heights: list[list[int]] = []
# if saved data, use that, else generate new data
try:
    # attempt to load the data file
    with open(data_folder + filename, "rb") as f:
        heights = pickle.load(f)
except:
    # generate the data
    for length in lengths:
        output = []
        model = Model(length)
        for i in range(number_cycles):
            model.cycle()
            output.append(model.get_pile_height())
        heights.append(output)
        # log progress, since this takes a while
        print("Length", length, "complete")

    # save the data
    with open(data_folder + filename, "wb") as f:
        pickle.dump(heights, f)

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

# linear plot
ax1 = fig.add_subplot(121)
for i in reversed(range(len(lengths))):
    ax1.plot(range(number_cycles), heights[i], label=str(
        lengths[i]), linewidth=1)
ax1.set_xlabel("Time, $t$")
ax1.set_ylabel("Pile Height, $h$")
ax1.set_xticklabels(['{:,}'.format(int(x)) for x in ax1.get_xticks().tolist()])
ax1.set_title("(A)")

# log-log plot
ax2 = fig.add_subplot(122)
for i in reversed(range(len(lengths))):
    ax2.plot(range(number_cycles), heights[i], label=str(
        lengths[i]), linewidth=1)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           borderaxespad=0., title="Size, $L$", markerscale=20)
ax2.set_xlabel("Time, $t$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_title("(B)")

# save the figure
plt.savefig(figures_folder + 'height_with_time.svg',
            format='svg', bbox_inches='tight')
