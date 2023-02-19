# Python 3.10.6
# =========================================================
# The model itself, used by all other scripts
# =========================================================

import numpy as np
import random
import matplotlib.pyplot as plt
from utils import figures_folder


class Model:
    def __init__(self, length: int, p: float = 0.5) -> None:
        """
        Initialise a new Oslo model of a given length
        Optionally set p, the probability of a threshold being 2
        rather than 1, default = 0.5 so 50:50 chance of 1 or 2.
        Setting p=0 leads to the Bak Tang & Wiesenfeld model.
        """
        # min system length of 3
        if length < 3:
            raise Exception("Min length is 3")
        self.length: int = length
        # generate empty gradient and threshold lists
        self.gradients: list[int] = [0] * length
        self.thresholds: list[int] = [0] * length
        # the system always starts in the transient state
        self.is_transient: bool = True
        # set the probability of threshold being 2 to p
        self.p = p
        # randomise each of the new threshold values
        for i in range(length):
            self.new_threshold(i)

    def get_length(self) -> int:
        """
        Get the length of the system.
        """
        return self.length

    def get_gradients(self) -> list[int]:
        """
        Get a list of all gradients.
        """
        return self.gradients

    def get_single_gradient(self, i: int) -> int:
        """
        Get a single gradient, at site `i`,
        where `i` starts from 0.
        """
        return self.gradients[i]

    def get_thresholds(self) -> list[int]:
        """
        Get a list of all thresholds.
        """
        return self.thresholds

    def get_single_threshold(self, i: int) -> int:
        """
        Get a single threshold at site `i`,
        where `i` starts from 0.
        """
        return self.thresholds[i]

    def get_all_heights(self) -> list[int]:
        """
        Get a list of all the heights.
        "All" is to indicate that this method
        requires running many computations rather than 
        accessing a class attribute.
        """
        heights: list[int] = []
        for i in range(len(self.gradients)):
            heights.append(self.get_height(i))
        return heights

    def get_height(self, i: int) -> int:
        """
        Get height at position `i`
        Where `i` starts from 0.
        """
        self.check_index_in_range(i)
        return np.sum(self.gradients[i:len(self.gradients)])

    def get_pile_height(self) -> int:
        """
        Get the height of the pile, i.e. the height of
        the pile at site `i == 0`.
        """
        return self.get_height(0)

    def get_is_transient(self) -> bool:
        """
        Get whether the model is in the transient phase.
        """
        return self.is_transient

    def check_index_in_range(self, i: int) -> None:
        """
        Check index `i` is within the range of the model.
        If not, raises an exception. 
        `i` can take values from `0` to `L-1`
        """
        if i >= self.length or i < 0:
            raise Exception("Index out of range")

    def new_threshold(self, i: int) -> None:
        """
        Set a new threshold at position `i`.
        The threshold will be 2 with chance `p` and 1 with
        chance `1-p`.
        """
        self.check_index_in_range(i)
        self.thresholds[i] = random.choices(
            population=[1, 2], weights=[1-self.p, self.p])[0]

    def drive(self) -> None:
        """
        Add a single grain to the first position
        """
        self.gradients[0] += 1

    def is_supercritical(self, i: int) -> bool:
        """
        Return whether position `i` is above the threshold.
        """
        self.check_index_in_range(i)
        return self.gradients[i] > self.thresholds[i]

    def relax(self, i: int) -> None:
        """
        Relax site `i`, assuming it is supercritical.
        """
        self.check_index_in_range(i)
        # update the gradients accordingly
        if i == 0:
            self.gradients[i] -= 2
            self.gradients[i+1] += 1
        elif i == self.length - 1:
            # end relaxation marks the transition to steady state
            if self.is_transient:
                self.is_transient = False
            self.gradients[i] -= 1
            self.gradients[i-1] += 1
        else:
            self.gradients[i] -= 2
            self.gradients[i-1] += 1
            self.gradients[i+1] += 1
        # ensure no values are below zero
        if self.gradients[i] < 0:
            self.gradients[i] = 0
        # reset threshold
        self.new_threshold(i)

    def cycle(self) -> None:
        """
        Perform one complete system cycle of driving and relaxation.
        """
        # add a grain to the first position
        self.drive()
        # relax all positions until stable
        pointer = 0
        # keep track of the right most avalanche site
        avalanche_limit = 0
        # if pointer to the right of the avalanche limit, no possible further avalanches
        while pointer < self.length and pointer <= avalanche_limit:
            # if this site is super critical
            if self.is_supercritical(pointer):
                # relax the site
                self.relax(pointer)
                # update the avalanche site to current site + 1
                avalanche_limit = max(avalanche_limit, pointer + 1)
                # update the pointer
                pointer -= 1
                if pointer < 0:
                    pointer = 0
            # if position not supercritical, move right by one
            else:
                pointer += 1

    def cycle_with_relax_count(self) -> int:
        """
        Perform one system cycle of driving and relaxation and return the 
        number of relaxations, i.e. the size of the avalanche.
        """
        # add a grain to the first position
        self.drive()
        # relax all positions until stable
        pointer = 0
        counter = 0
        while pointer < self.length:
            if self.is_supercritical(pointer):
                self.relax(pointer)
                # difference to regular cycle is this counter
                counter += 1
                pointer -= 1
                if pointer < 0:
                    pointer = 0
            else:
                pointer += 1
        # check values aren't approaching the 32 bit limit
        if counter > 2e9:
            raise Exception("Counter approaching 32 bit limit")
        return counter

    def cycle_with_transition_counts(self) -> dict[int, dict[int, int]]:
        """
        Perform one system cycle and return counts of each threshold transition,
        including sites adjacent to a relaxation which didn't exceed criticality.
        """
        # setup a dictionary to store the counts
        counts = {
            1: {
                1: 0,
                2: 0
            },
            2: {
                1: 0,
                2: 0
            }
        }
        # add a grain to the first position
        self.drive()
        # relax all positions until stable
        pointer = 0
        while pointer < self.length:
            if self.is_supercritical(pointer):
                # given current site is supercritical, count the transition
                initial_threshold = self.get_single_threshold(pointer)
                self.relax(pointer)
                final_threshold = self.get_single_threshold(pointer)
                counts[initial_threshold][final_threshold] += 1
                # given a relaxation just occurred, count adjacent sites only if
                # sub critical, else they'll be counted twice when they relax
                if pointer > 0 and pointer < self.length - 1:
                    if not self.is_supercritical(pointer-1):
                        threshold = self.get_single_threshold(pointer-1)
                        counts[threshold][threshold] += 1
                    if not self.is_supercritical(pointer+1):
                        threshold = self.get_single_threshold(pointer+1)
                        counts[threshold][threshold] += 1

                pointer -= 1
                if pointer < 0:
                    pointer = 0
            else:
                pointer += 1
        return counts

    def plot(self, save_as: str = "plot.svg") -> None:
        """
        Plot the current state of the system and save it to an svg.
        """
        # get the current state of the system
        heights = self.get_all_heights()
        # construct a figure
        fig = plt.figure(figsize=(3, 6))
        ax = fig.add_subplot(111)
        # plot the heights as a bar chart
        ax.bar(np.array(range(self.length)) + 1,
               heights, width=0.95, color='grey')
        ax.axis('scaled')
        ax.set_ylabel("Height")
        ax.set_xlabel("Site, $i$")
        if len(heights) <= 8:
            ax.set_yticks(range(max(heights) + 1))
            ax.set_xticks(np.array(range(self.length)) + 1)
            ax.grid(axis='y')
        plt.savefig(figures_folder + save_as,
                    format='svg', bbox_inches='tight')
