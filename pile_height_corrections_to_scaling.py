# Python 3.10.6
# =========================================================
# Generate the corrections to scaling plot
# =========================================================

from generate_heights import get_heights_data
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from utils import figures_folder

# =========================================================
# get data
# =========================================================
lengths, height_sequence_list = get_heights_data()

average_height_list = []
average_height_errors = []
for l in height_sequence_list:
    average_height_list.append(np.average(l))
    average_height_errors.append(np.std(l)/np.sqrt(len(l)))
print("Lengths:", lengths)
print("Errors:", average_height_errors)

# =========================================================
# fitting
# =========================================================


def corrections_to_scaling_func(L, a0, a1, o1):
    return a0 * (1 - a1 * L ** (-o1))


def full_scaling_func(L, a0, a1, o1):
    return a0 * L * (1 - a1 * L ** (-o1))


scaled_values = [average_height_list[i] / lengths[i]
                 for i in range(len(lengths))]

popt, pcov = curve_fit(corrections_to_scaling_func, lengths, scaled_values)
x_min, x_max = 0.1, 600
x_vals = np.linspace(x_min, x_max, 100)

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

# left
ax1 = fig.add_subplot(121)
ax1.scatter(lengths, average_height_list, s=50, marker="+",  # type: ignore
            c="k", label="Data")  # type: ignore
ax1.plot(x_vals, full_scaling_func(x_vals, *popt), color='lightgrey',
         linestyle='dashed', label='Full Fit', zorder=-1)
ax1.legend(loc='lower right')
ax1.set_xlabel("System Length, $L$")
ax1.set_ylabel(r"$\langle h \rangle_t$")
x1, _ = ax1.get_xlim()
y1, _ = ax1.get_ylim()
ax1.set_xlim(x1, x_max)
ax1.set_ylim(y1, full_scaling_func(x_max, *popt))
ax1.set_title("(A)")

# right
ax2 = fig.add_subplot(122)
ax2.scatter(lengths, scaled_values, s=50, marker="+",  # type: ignore
            c="k", label="Data")
ax2.plot(x_vals, corrections_to_scaling_func(x_vals, *popt),
         label="Cor. to Scaling Fit", color="lightgrey", linestyle='dashed', zorder=-1)
x1, _ = ax2.get_xlim()
ax2.hlines(popt[0], x1, x_max, color='k',
           linestyle='dotted', label="Asymptote, $a_0$")
ax2.set_xlim(x1, x_max)
ax2.set_ylim(1.55, 1.75)
ax2.set_yticks([1.55, 1.60, 1.65, 1.70, 1.75])
print("Fit: a0 = %.3f +/- %.3f, a1 = %.3f +/- %.3f, o1 = %.3f +/- %.3f" %
      (popt[0], np.sqrt(pcov[0, 0]), popt[1], np.sqrt(pcov[1, 1]), popt[2], np.sqrt(pcov[2, 2])))
ax2.legend()
ax2.set_xlabel("System Length, $L$")
ax2.set_ylabel(r"$\langle h \rangle_t \,\, / \,\, L$")
ax2.set_title("(B)")

plt.savefig(figures_folder + 'corrections_to_scaling.svg',
            format='svg', bbox_inches='tight')
