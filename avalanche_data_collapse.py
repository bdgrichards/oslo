# Python 3.10.6
# =========================================================
# Generate the avalanche data collapse plot
# =========================================================

import matplotlib.pyplot as plt
from utils import figures_folder
from generate_avalanches import get_avalanches_data
from logbin import logbin

# =========================================================
# parameters
# =========================================================
scale = 1.2  # logbin scale
# data collapse parameters
tau_s = 1.56
D = 2.19

# =========================================================
# get data
# =========================================================
lengths, avalanches_list = get_avalanches_data()

# since finite scaling ansatz only valid for L >> 1
# ignoring L = 4 & 8
lengths = lengths[2:]
avalanches_list = avalanches_list[2:]

# =========================================================
# logbin data
# =========================================================
log_binned_avalanches_x = []
log_binned_avalanches_y = []
for i in avalanches_list:
    x_vals, y_vals = logbin(i, scale=scale, zeros=False)
    log_binned_avalanches_x.append(x_vals)
    log_binned_avalanches_y.append(y_vals)

# =========================================================
# data collapse
# =========================================================
# multiplying each of the the y values by s^tau_s
scaled_avalanches_y = []
for i in range(len(log_binned_avalanches_y)):
    scaled_avalanche = []
    for j in range(len(log_binned_avalanches_y[i])):
        scaled_avalanche.append(
            log_binned_avalanches_y[i][j] * log_binned_avalanches_x[i][j]**(tau_s))
    scaled_avalanches_y.append(scaled_avalanche)
# dividing each of the the x values by L^D
scaled_avalanches_x = []
for i in range(len(log_binned_avalanches_x)):
    scaled_avalanches_x.append(log_binned_avalanches_x[i] / (lengths[i]**D))


# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

ax1 = fig.add_subplot(111)
for i in reversed(range(len(lengths))):
    ax1.scatter(
        scaled_avalanches_x[i], scaled_avalanches_y[i], s=1, label=str(lengths[i]))
    ax1.plot(scaled_avalanches_x[i], scaled_avalanches_y[i], alpha=0.2)
ax1.set_yscale('log')
ax1.set_xscale('log')
ax1.set_xlabel(r'$s \, / \, L^D$')
ax1.set_ylabel(r'$s^{\tau_s} \,\, \tilde{P} \, (s;L)$')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           borderaxespad=0., markerscale=5, title=r"Size, $L$")

plt.savefig(figures_folder + 'avalanche_collapse.svg',
            format='svg', bbox_inches='tight')
