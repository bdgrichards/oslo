from utils import figures_folder
from generate_heights import get_heights_data
import matplotlib.pyplot as plt

# =========================================================
# get data
# =========================================================
lengths, height_sequence_list = get_heights_data()

# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

ax1 = fig.add_subplot(111)
for i in reversed(range(len(lengths))):
    data = height_sequence_list[i]
    n, bins, patches = plt.hist(data, max(data) - min(data) + 1, density=True,
                                range=(min(data)-0.5, max(data)+0.5), alpha=0.1)
    bin_means = [0.5 * (bins[i] + bins[i+1]) for i in range(len(n))]
    ax1.plot(bin_means, n, color="C%i" %
             (len(lengths) - i - 1), label=lengths[i])
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           borderaxespad=0., title="Size, $L$")
ax1.set_xlabel("Pile Height, $h$")
ax1.set_xlim(-15, 950)
ax1.set_ylim(0, 0.5)
ax1.set_ylabel(r"$P \, (h;L)$")

plt.savefig(figures_folder + 'all_prob_distributions.svg',
            format='svg', bbox_inches='tight')
