from utils import figures_folder
from generate_avalanches import get_avalanches_data
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from logbin import logbin
import matplotlib as mpl

# =========================================================
# parameters
# =========================================================
scale = 1.2  #  logbin scale

# =========================================================
# get data
# =========================================================
lengths, avalanches_list = get_avalanches_data()

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
# plotting
# =========================================================
# when dealining with large amounts of data
mpl.rcParams['agg.path.chunksize'] = 10000

fig = plt.figure(figsize=(6.5, 3), tight_layout=True)
gs = gridspec.GridSpec(1, 3)

# log-linear plot of raw data
ax1 = fig.add_subplot(gs[0, 0])
for i in reversed(range(len(lengths))):
    ax1.plot(range(len(avalanches_list[i])),
             avalanches_list[i], label=str(lengths[i]), rasterized=True)
ax1.set_xlabel("$t$")
ax1.set_ylabel("Avalanche Size, $s$")
ax1.set_yscale('log')
ax1.set_xlim(0, 1000000)
ax1.set_xticks([0, 500000, 1000000])
ax1.ticklabel_format(axis='x', style='sci', scilimits=(0, 0), useMathText=True)
ax1.set_title("(A)")

ax2 = fig.add_subplot(gs[0, 1:])
for i in reversed(range(len(lengths))):
    ax2.scatter(
        log_binned_avalanches_x[i], log_binned_avalanches_y[i], s=1, label=str(lengths[i]))
    ax2.plot(
        log_binned_avalanches_x[i], log_binned_avalanches_y[i], alpha=0.2, rasterized=True)
ax2.set_yscale('log')
ax2.set_xscale('log')
ax2.set_xlabel("Avalanche Size, $s$")
ax2.set_ylabel(r'$\tilde{P}_N \,(s;L)$')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           borderaxespad=0., markerscale=5, title=r"Size, $L$")
ax2.set_title("(B)")

plt.savefig(figures_folder + 'avalanche_probs.svg',
            format='svg', bbox_inches='tight', dpi=300)
