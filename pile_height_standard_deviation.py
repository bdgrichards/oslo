from utils import figures_folder
from generate_heights import get_heights_data
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# =========================================================
# get data
# =========================================================
lengths, height_sequence_list = get_heights_data()
std_values = [np.std(data) for data in height_sequence_list]

# =========================================================
# fitting
# =========================================================


def std_cts_func(L, a0, o1):
    return a0 * L ** o1


popt, pcov = curve_fit(std_cts_func, lengths, std_values)
x_vals = np.linspace(4, 600, 100)
print("Fit: a0 = %.2f, o1 = %.2f" % (popt[0], popt[1]))

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

# linear plot
ax1 = fig.add_subplot(121)
ax1.scatter(lengths, std_values, s=50,
            marker="+", c="k", label="Data")  # type: ignore
ax1.plot(x_vals, std_cts_func(x_vals, *popt), label=r"Fit",
         color='lightgrey', linestyle='dashed', zorder=-1)
ax1.set_xlabel("System Length, $L$")
ax1.set_ylabel(r"Standard Deviation, $\sigma_h$")
ax1.set_title("(A)")

# log-log plot
ax2 = fig.add_subplot(122)
ax2.scatter(lengths, std_values, s=50,
            marker="+", c="k", label="Data")  # type: ignore
ax2.plot(x_vals, std_cts_func(x_vals, *popt), label="Fit",
         color='lightgrey', linestyle='dashed', zorder=-1)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax2.set_xlabel("System Length, $L$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_yticks([1, 2, 3])
ax2.set_title("(B)")

plt.savefig(figures_folder + 'standard_deviation.svg',
            format='svg', bbox_inches='tight')
