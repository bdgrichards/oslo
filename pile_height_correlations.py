from model import Model
import numpy as np
import pickle
import matplotlib.pyplot as plt
from utils import data_folder, figures_folder

# =========================================================
# parameters
# =========================================================
length = 512
repetitions = 20
# to ensure the samples aren't biased by being at the transition point
cycles_after_transient = 1000
min_sep, max_sep = 1, 20
filename = 'correlation_gradients.pickle'

# =========================================================
# get data
# =========================================================
gradients: list[list[int]] = []
# if saved data, use that, else generate new data
try:
    # attempt to load the data file
    with open(data_folder + filename, "rb") as f:
        gradients = pickle.load(f)
except:
    # generate the data
    for rep in range(repetitions):
        # initiate model
        model = Model(length)
        # run model
        while model.get_is_transient():
            model.cycle()
        for _ in range(cycles_after_transient):
            model.cycle()
        # get gradients
        gradients.append(model.get_gradients())
        # log progress, since this takes a while
        print("Rep", rep + 1, "of", repetitions, "complete")

    # saving
    with open(data_folder + filename, "wb") as f:
        pickle.dump(gradients, f)


# =========================================================
# calculate correlations
# =========================================================
# setup the list of separations we want to measure
separations: list[int] = []
for i in range(min_sep, max_sep + 1):
    separations.append(i)

# setup a way to save the values of the correlations
correlations = {}
for s in separations:
    correlations[s] = []

# repeat calculations for each repetition
for rep in range(len(gradients)):
    single_grad_list = gradients[rep]

    # measure the correlations
    for s in separations:
        # create the two arrays to correlate
        y = single_grad_list[0:len(single_grad_list)-s]
        x = single_grad_list[s:len(single_grad_list)]
        # find the correlation coefficient between them
        corr = np.corrcoef(x, y)[0][1]
        # save the correlation
        correlations[s].append(corr)

correlation_means = []
errors = []

# extract the mean and std
for s in separations:
    correlation_means.append(np.mean(correlations[s]))
    errors.append(np.std(correlations[s]))


# =========================================================
# plotting
# =========================================================
fig = plt.figure(figsize=(6.5, 3), layout="constrained")

ax1 = fig.add_subplot(111)
ax1.errorbar(separations, correlation_means,
             yerr=errors, fmt='o', capsize=3, c='k')
ax1.set_xlabel("Separation, $s$")
ax1.set_ylabel(r"Pearson Correlation, $\rho$")
ax1.set_xticks(separations)
ax1.hlines([0], [separations[0] - 0.5],
           [separations[-1] + 0.5], color='k', linestyle='dashed')
ax1.set_xlim(separations[0] - 0.5, separations[-1] + 0.5)

plt.savefig(figures_folder + 'correlations.svg',
            format='svg', bbox_inches='tight')
