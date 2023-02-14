import numpy as np
from utils import data_folder, figures_folder
from model import Model
import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# =========================================================
# parameters
# =========================================================
lengths = [4, 8, 16, 32, 64, 128, 256, 512]
repetitions = 10
filename = 'cross_over_times.pickle'

# =========================================================
# get data
# =========================================================
cross_over_times = []
# if saved data, use that, else generate new data
try:
    # attempt to load the data file
    with open(data_folder + filename, "rb") as f:
        cross_over_times = pickle.load(f)
except:
    # generate the data
    for length in lengths:
        times = []
        for i in range(repetitions):
            model = Model(length)
            # if a grain exits on the first cycle, counter should be 0
            # since we are measuring total grains *before* an exit
            counter = -1
            while model.get_is_transient():
                model.cycle()
                counter += 1
            times.append(counter)
        cross_over_times.append(np.average(times))
        # log progress, since this takes a while
        print("Length", length, "complete")

        # save the data
        with open(data_folder + filename, "wb") as f:
            pickle.dump(cross_over_times, f)

# =========================================================
# fitting
# =========================================================


# the function we want to fit
def squared_func(x, a):
    return a*x**2


# fit the function
popt, pcov = curve_fit(squared_func, lengths, cross_over_times)
# generate the x and y values for plotting
fit_x_vals = np.linspace(3.5, 600, 1000)
fit_y_vals = squared_func(fit_x_vals, *popt)
# output the final parameters
print("Fit: %.2f * x^2" % popt[0])

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

# linear plot
ax1 = fig.add_subplot(121)
ax1.scatter(lengths, cross_over_times, s=50,
            marker="+", c="k", label="Data")  # type: ignore
ax1.plot(fit_x_vals, fit_y_vals, label=r"$ax^2$ Fit",
         color='lightgrey', linestyle='dashed', zorder=-1)
ax1.set_xlabel("System Length, $L$")
ax1.set_ylabel(r"Average Cross-Over Time, $\langle t_c \rangle$")
ax1.ticklabel_format(axis='y', style='sci', scilimits=(3, 3), useMathText=True)
ax1.set_title("(A)")

# log-log plot
ax2 = fig.add_subplot(122)
ax2.scatter(lengths, cross_over_times, s=50,
            marker="+", c="k", label="Data")  # type: ignore
ax2.plot(fit_x_vals, fit_y_vals, label=r"$ax^2$ Fit",
         color='lightgrey', linestyle='dashed', zorder=-1)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           borderaxespad=0.)
ax2.set_xlabel("System Length, $L$")
ax2.set_xscale("log")
ax2.set_yscale("log")
ax2.set_title("(B)")

plt.savefig(figures_folder + 'cross_over_times.svg',
            format='svg', bbox_inches='tight')
