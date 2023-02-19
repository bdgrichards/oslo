# Python 3.10.6
# =========================================================
# Generate the Gaussian data collapse plot
# =========================================================

from utils import figures_folder
from generate_heights import get_heights_data
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import skew

# =========================================================
# get data
# =========================================================
lengths, height_sequence_list = get_heights_data()

# =========================================================
# plotting
# =========================================================


def collapse_func(x):
    return (1 / np.sqrt(2*np.pi)) * np.exp(-0.5*x**2)


# x values to plot the fitted function against
x_min, x_max = -7, 7
x_vals = np.linspace(x_min, x_max, 100)

fig = plt.figure(figsize=(6.5, 3), layout="constrained")

# linear plot
ax1 = fig.add_subplot(121)
for i in reversed(range(len(lengths))):
    data = height_sequence_list[i]
    average = np.average(data)
    std = np.std(data)
    n, bins, patches = plt.hist(data, max(data) - min(data) + 1, density=True,
                                range=(min(data)-0.5, max(data)+0.5), alpha=0)
    bin_means = [0.5 * (bins[i] + bins[i+1]) for i in range(len(n))]
    scaled_n = np.array(n)*std
    scaled_bin_means = [(bin_mean - average)/std for bin_mean in bin_means]
    ax1.scatter(scaled_bin_means, scaled_n, s=20, color="C%i" % (
        len(lengths) - i - 1), label="$L=$%i" % lengths[i], marker="x")  # type: ignore
ax1.plot(x_vals, collapse_func(x_vals), color='k',
         label='CLT', linestyle='dashed')
ax1.set_xlabel(r"$\frac{h - \langle h \rangle}{\sigma_h}$")
ax1.set_ylabel(r"$\sigma_h \,\, P \, (h;L)$")
ax1.set_xlim(x_min, x_max)
ax1.set_title("(A)")

# difference plot
ax2 = fig.add_subplot(122)
values_for_skewness = []
for i in reversed(range(len(lengths))):
    data = height_sequence_list[i]
    average = np.average(data)
    std = np.std(data)
    n, bins, patches = plt.hist(data, max(data) - min(data) + 1, density=True,
                                range=(min(data)-0.5, max(data)+0.5), alpha=0)
    bin_means = [0.5 * (bins[i] + bins[i+1]) for i in range(len(n))]
    scaled_n = np.array(n)*std
    scaled_bin_means = [(bin_mean - average)/std for bin_mean in bin_means]
    diff_n = []
    # subtracting the expected values
    for index in range(len(scaled_n)):
        diff_n.append(
            (scaled_n[index] / collapse_func(scaled_bin_means[index]))-1)
    ax2.scatter(scaled_bin_means, diff_n, s=20, color="C%i" % (
        len(lengths) - i - 1), label="$L=$%i" % lengths[i], marker="x")  # type: ignore
    # add the x values to the overall list for skewness calculation
    values_for_skewness += scaled_bin_means
# calculate skewness
total_skew = skew(values_for_skewness)
print("Skew:", total_skew)
# plot
ax2.plot(x_vals, [0 for _ in x_vals], color='k',
         label=r"CLT, $\mathcal{E}$", linestyle='dashed')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax2.set_xlabel("System Length, $L$")
ax2.set_ylabel(
    r"$(\sigma_h \, P - \mathcal{E}) \, / \, \mathcal{E}$")
ax2.set_xlabel(r"$\frac{h - \langle h \rangle}{\sigma_h}$")
ax2.set_xlim(x_min, x_max)
ax2.set_yscale("symlog", linthresh=0.1)
ax2.hlines([0.1, -0.1], x_min, x_max,
           color='lightgrey', linewidth=1, zorder=-1)
ax2.set_title("(B)")

plt.savefig(figures_folder + 'gaussian_data_collapse.svg',
            format='svg', bbox_inches='tight')
