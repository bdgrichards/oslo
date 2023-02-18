from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from utils import data_folder, figures_folder, average_different_lengths
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from model import Model
import numpy as np
import pickle

# =========================================================
# parameters
# =========================================================
lengths = [4, 8, 16, 32, 64, 128, 256, 512]
repetitions = 20
filename = 'average_heights_with_time.pickle'

# =========================================================
# get data
# =========================================================
average_heights_with_time: list[list[int]] = []
# if saved data, use that, else generate new data
try:
    # attempt to load the data file
    with open(data_folder + filename, "rb") as f:
        average_heights_with_time = pickle.load(f)
except:
    # generate the data
    for length in lengths:
        height_lists: list[list[int]] = []
        for _ in range(repetitions):
            model = Model(length)
            height_values: list[int] = []
            # run for 1.5 * max cross over time
            for _ in range(int(1.5*length**2)):
                model.cycle()
                height_values.append(model.get_pile_height())
            height_lists.append(height_values)
        average_heights_with_time.append(
            average_different_lengths(height_lists))
        # log progress, since this takes a while
        print("Length", length, "complete")

    # save the data
    with open(data_folder + filename, "wb") as f:
        pickle.dump(average_heights_with_time, f)

# =========================================================
# data collapse
# =========================================================


# fit the proposed scaling function
def scaling_func(x, g):
    try:
        x[0]
        results = []
        for x_i in x:
            if x_i < 0.5*g:
                results.append((2*g*x_i) ** 0.5)
            else:
                results.append(g)
        return results
    except:
        if x < 0.5*g:
            return (2*g*x) ** 0.5
        else:
            return g


# generate values for fitting
y_vals = [np.array(i) for i in average_heights_with_time]
x_vals = [np.array(range(len(average_heights_with_time[i])))/(lengths[i]**2)
          for i in range(len(average_heights_with_time))]

# divide each of the y_vals by their system length
for i in range(len(y_vals)):
    y_vals[i] = y_vals[i] / lengths[i]

# fitting
popt, pcov = curve_fit(scaling_func, x_vals[-1], y_vals[-1])
fit_x_vals = np.linspace(0.00001, 1.5, 100000)
fit_y_vals = scaling_func(fit_x_vals, *popt)
print("Fit: g = %.3f" % popt[0])

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

# linear
ax1 = fig.add_subplot(121)
ax1.plot(fit_x_vals, fit_y_vals,
         linestyle='dashed', c='k', linewidth=2)
for i in range(len(lengths)):
    ax1.scatter(x_vals[i], y_vals[i], label=str(
        lengths[i]), s=1, c="C%i" % (len(lengths) - i - 1), rasterized=True)
ax1.set_xlabel(r"$t \, / \, L^2$")
ax1.set_ylabel(r"$\tilde{h}(t;L) \, / \, L$")
ax1.set_title("(A)")

# logarithmic
ax2 = fig.add_subplot(122)
ax2.plot(fit_x_vals, fit_y_vals, label='Fit',
         linestyle='dashed', c='k', linewidth=2)
for i in range(len(lengths)):
    ax2.scatter(x_vals[i], y_vals[i], label=str(
        lengths[i]), s=1, c="C%i" % (len(lengths) - i - 1), rasterized=True)
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(reversed(handles), reversed(labels), bbox_to_anchor=(
    1.05, 1), loc='upper left', borderaxespad=0., title="Size, $L$", markerscale=4)
ax2.set_xlabel(r"$t \, / \, L^2$")
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_title("(B)")

# zoom in region
x1, x2 = 0.5, 1.7
y1, y2 = 1.1, 1.9

ax2ins = zoomed_inset_axes(ax2, 5, loc=4)
ax2ins.plot(fit_x_vals, fit_y_vals, label='Fit',
            linestyle='dashed', c='k', linewidth=2)
for i in range(len(lengths)):
    ax2ins.scatter(x_vals[i], y_vals[i], label=str(
        lengths[i]), s=1, c="C%i" % (len(lengths) - i - 1), rasterized=True)
ax2ins.set_xlim(x1, x2)
ax2ins.set_ylim(y1, y2)
ax2ins.set_xticks([])
ax2ins.set_yticks([])
mark_inset(ax2, ax2ins, loc1=2, loc2=1, fc="none", ec="0.5")
plt.draw()

plt.savefig(figures_folder + 'data_collapse.svg',
            format='svg', bbox_inches='tight', dpi=300)
