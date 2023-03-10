# Python 3.10.6
# =========================================================
# Generate the avalanche moments plot
# =========================================================

from generate_avalanches import get_avalanches_data
import matplotlib.pyplot as plt
from utils import figures_folder
from scipy.optimize import curve_fit
import numpy as np

# =========================================================
# parameters
# =========================================================
all_moments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# for single moments, or initial guesses
moments_to_plot = [1, 2, 3, 4]

# =========================================================
# get data
# =========================================================
lengths, avalanches_list = get_avalanches_data()

# since finite scaling ansatz only valid for L >> 1
# ignoring L = 4 & 8
lengths = lengths[2:]
avalanches_list = avalanches_list[2:]

# =========================================================
# calculate moments
# =========================================================


def calculate_moment(data, order):
    scaled_data = [i**order for i in data]
    return sum(scaled_data) / len(data)


# calculate the moments
moments_values = []
for m in moments_to_plot:
    y_vals = []
    for l in range(len(lengths)):
        y_vals.append(calculate_moment(avalanches_list[l], m))
    moments_values.append(y_vals)

# =========================================================
# fitting the moments
# =========================================================


def power_law_func(L, a0, a1):
    try:
        L[0]
        results = []
        for L_i in L:
            results.append(a0 * L_i ** a1)
        return results
    except:
        return a0 * L ** a1


fit_data = []
a1_errors = []
initial_guesses = [
    [1, 1],  # 1
    [0.2, 3.2],  # 2
    [0.1, 5],  # 3
    [0.01, 8],  # 4
]
for m in range(len(moments_to_plot)):
    popt, pcov = curve_fit(power_law_func, lengths,
                           moments_values[m], p0=initial_guesses[all_moments.index(moments_to_plot[m])], method='dogbox', max_nfev=100000)
    fit_data.append(popt)
    a1_errors.append(np.sqrt(pcov[1][1]))
print(a1_errors)

# =========================================================
# fitting the fits
# =========================================================
# extract the correct values from the fit data
y_vals = [i[1] for i in fit_data]
x_vals = moments_to_plot


def linear_func(k, a, b):
    try:
        k[0]
        results = []
        for k_i in k:
            results.append(a + b*k_i)
        return results
    except:
        return a + b*k


# fit a straight line to the data
popt, pcov = curve_fit(linear_func, x_vals, y_vals)
print("Fit: %.2f + %.2f * k" % (popt[0], popt[1]))
D = popt[1]
D_err = np.sqrt(pcov[1, 1])
Ts = 1 - (popt[0]/popt[1])
# propagation by quadrature
Ts_err = Ts * np.sqrt((np.sqrt(pcov[0, 0])/popt[0])
                      ** 2 + (np.sqrt(pcov[1, 1])/popt[1])**2)
print("D: %.3f" % D)
print("D error: %.3f" % D_err)
print("Ts: %.3f" % Ts)
print("Ts error: %.3f" % Ts_err)

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), tight_layout=True)
# we don't want to use exactly the same order of colours
# as we have done for system size
color_shift = 5

ax1 = fig.add_subplot(121)
for m in range(len(moments_to_plot)):
    ax1.scatter(lengths, moments_values[m], c="C%s" % (
        m + color_shift), label="k = %s" % (moments_to_plot[m]), marker='+', s=50)  # type: ignore
    ax1.plot(lengths, power_law_func(
        lengths, *fit_data[m]), color="C%s" % (m + color_shift), alpha=0.3)
ax1.set_xlabel("System Size, $L$")
ax1.set_ylabel(r"$\langle \, s^k \, \rangle$")
ax1.set_yscale("log")
ax1.set_xscale("log")
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
ax1.set_title("(A)")

ax2 = fig.add_subplot(122)
ax2.scatter(x_vals, y_vals, c='k', label='Values',
            marker='+', s=50)  # type: ignore
ax2.plot(x_vals, linear_func(
    x_vals, popt[0], popt[1]), c='grey', zorder=-1, label='Fit')
ax2.set_xlabel("$k$")
ax2.set_ylabel(r"$D \, (1 + k - \tau_s)$")
ax2.legend()
ax2.set_title("(B)")

plt.savefig(figures_folder + 'moments.svg', format='svg', bbox_inches='tight')
