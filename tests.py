from model import Model
import numpy as np

# =========================================================
# plotting tests
# =========================================================


def test_1():
    """
    Test that an empty system is generated after initialisation.
    """
    model = Model(4)
    model.plot("test.svg")
# test_1()


def test_2():
    """
    Test that a single cycle of the model acts as expected.
    """
    model = Model(4)
    model.cycle()
    model.plot("test.svg")
# test_2()


def test_3():
    """
    Test that a relaxation works as expected, setting p to 0.
    """
    model = Model(4, p=0)
    model.cycle()
    model.cycle()
    model.plot("test.svg")
# test_3()


def test_4():
    """
    Test that a p=0 model reaches steady state.
    """
    model = Model(4, p=0)
    while model.get_is_transient():
        model.cycle()
    model.plot("test.svg")
# test_4()


def test_5():
    """
    Test that a p=0.5 model reaches steady state.
    """
    model = Model(4)
    while model.get_is_transient():
        model.cycle()
    model.plot("test.svg")
# test_5()


def test_6():
    """
    Test that a large, L=128 p=0.5 model reaches steady state.
    """
    model = Model(128)
    while model.get_is_transient():
        model.cycle()
    model.plot("test.svg")
# test_6()

# =========================================================
# output tests
# =========================================================


def test_7():
    """
    Test every class method on a p=0 model that isn't tested 
    by the plotting tests
    """
    model = Model(4, p=0)

    # test non-getter methods
    in_range_1 = model.check_index_in_range(0)
    in_range_2 = model.check_index_in_range(3)
    print("Testing Index Range Checker")
    print("1: Expected: None")
    print("   Measured:", in_range_1)
    print("2: Expected: None")
    print("   Measured:", in_range_2)

    print("3: Expected: Exception")
    try:
        model.check_index_in_range(-1)
        print("   Measured: NO Exception")
    except:
        print("   Measured: Exception")

    print("4: Expected: Exception")
    try:
        model.check_index_in_range(4)
        print("   Measured: NO Exception")
    except:
        print("   Measured: Exception")

    # test getters before a cycle
    length_0 = model.get_length()
    gradients_0 = model.get_gradients()
    single_gradient_0 = model.get_single_gradient(0)
    thresholds_0 = model.get_thresholds()
    single_threshold_0 = model.get_single_threshold(0)
    heights_0 = model.get_all_heights()
    single_height = model.get_height(0)
    pile_height_0 = model.get_pile_height()
    is_transient_0 = model.get_is_transient()

    print("5: Expected: 4")
    print("   Measured:", length_0)
    print("6: Expected: [0, 0, 0, 0]")
    print("   Measured:", gradients_0)
    print("7: Expected: 0")
    print("   Measured:", single_gradient_0)
    print("8: Expected: [1, 1, 1, 1]")
    print("   Measured:", thresholds_0)
    print("9: Expected: 1")
    print("   Measured:", single_threshold_0)
    print("10 Expected: [0, 0, 0, 0]")
    print("   Measured:", heights_0)
    print("11 Expected: 0")
    print("   Measured:", single_height)
    print("12 Expected: 0")
    print("   Measured:", pile_height_0)
    print("13 Expected: True")
    print("   Measured:", is_transient_0)

    # measure all of the getters after one cycle
    model.cycle()

    length_0 = model.get_length()
    gradients_0 = model.get_gradients()
    single_gradient_0 = model.get_single_gradient(0)
    thresholds_0 = model.get_thresholds()
    single_threshold_0 = model.get_single_threshold(0)
    heights_0 = model.get_all_heights()
    single_height = model.get_height(0)
    pile_height_0 = model.get_pile_height()
    is_transient_0 = model.get_is_transient()

    print("14 Expected: 4")
    print("   Measured:", length_0)
    print("15 Expected: [1, 0, 0, 0]")
    print("   Measured:", gradients_0)
    print("16 Expected: 1")
    print("   Measured:", single_gradient_0)
    print("17 Expected: [1, 1, 1, 1]")
    print("   Measured:", thresholds_0)
    print("18 Expected: 1")
    print("   Measured:", single_threshold_0)
    print("19 Expected: [1, 0, 0, 0]")
    print("   Measured:", heights_0)
    print("20 Expected: 1")
    print("   Measured:", single_height)
    print("21 Expected: 1")
    print("   Measured:", pile_height_0)
    print("22 Expected: True")
    print("   Measured:", is_transient_0)

    # measure all of the getters after two cycles
    model.cycle()

    length_0 = model.get_length()
    gradients_0 = model.get_gradients()
    single_gradient_0 = model.get_single_gradient(0)
    thresholds_0 = model.get_thresholds()
    single_threshold_0 = model.get_single_threshold(0)
    heights_0 = model.get_all_heights()
    single_height = model.get_height(0)
    pile_height_0 = model.get_pile_height()
    is_transient_0 = model.get_is_transient()

    print("23 Expected: 4")
    print("   Measured:", length_0)
    print("24 Expected: [0, 1, 0, 0]")
    print("   Measured:", gradients_0)
    print("25 Expected: 0")
    print("   Measured:", single_gradient_0)
    print("26 Expected: [1, 1, 1, 1]")
    print("   Measured:", thresholds_0)
    print("27 Expected: 1")
    print("   Measured:", single_threshold_0)
    print("28 Expected: [1, 1, 0, 0]")
    print("   Measured:", heights_0)
    print("29 Expected: 1")
    print("   Measured:", single_height)
    print("30 Expected: 1")
    print("   Measured:", pile_height_0)
    print("31 Expected: True")
    print("   Measured:", is_transient_0)
# test_7()


def test_8():
    """
    Test that thresholds are distributed correctly.
    """
    # for p = 1
    model = Model(1024, p=1)
    # count the thresholds
    counts = {
        1: 0,
        2: 0,
    }
    for i in model.get_thresholds():
        counts[i] += 1
    print("For p=1:")
    print("Expected thresholds:", {1: 0, 2: 1024})
    print("Measured thresholds:", counts)

    # for p = 0
    model = Model(1024, p=0)
    # count the thresholds
    counts = {
        1: 0,
        2: 0,
    }
    for i in model.get_thresholds():
        counts[i] += 1
    print("For p=0:")
    print("Expected thresholds:", {1: 1024, 2: 0})
    print("Measured thresholds:", counts)

    # for p = 0.5
    model = Model(1024)
    # count the thresholds
    counts = {
        1: 0,
        2: 0,
    }
    for i in model.get_thresholds():
        counts[i] += 1
    print("For p=0.5: (approx)")
    print("Expected thresholds:", {1: 512, 2: 512})
    print("Measured thresholds:", counts)
# test_8()


def test_9():
    """
    Test cycle_with_relax_count for a p=0 model
    """
    counts = []
    model = Model(8, p=0)
    for _ in range(5):
        counts.append(model.cycle_with_relax_count())
    print("Expected: [0, 1, 0, 2, 1]")
    print("Measured:", counts)
# test_9()


def test_10():
    """
    Test cycle_with_transition_counts for a p=0 model
    """
    counts = []
    model = Model(8, p=0)
    for _ in range(2):
        counts.append(model.cycle_with_transition_counts())
    print(
        "Expected: [{1: {1: 0, 2: 0}, 2: {1: 0, 2: 0}}, {1: {1: 1, 2: 0}, 2: {1: 0, 2: 0}}]")
    print("Measured:", counts)
# test_10()

# =========================================================
# example tests
# =========================================================


def test_11():
    """"
    The first of the two recommended tests from the lab manual, for L = 16.
    """
    final_heights = []
    test_model = Model(16)
    # get to steady state
    while test_model.get_is_transient():
        test_model.cycle()
    # once in steady state run for a set number of trials
    for _ in range(100000):
        test_model.cycle()
        final_heights.append(test_model.get_pile_height())
    print("Expected: 26.5, measured: %.2f" % np.average(final_heights))
# test_11()


def test_12():
    """"
    The second of the two recommended tests from the lab manual, for L = 32.
    """
    final_heights = []
    test_model = Model(32)
    # get to steady state
    while test_model.get_is_transient():
        test_model.cycle()
    # once in steady state run for a set number of trials
    for _ in range(100000):
        test_model.cycle()
        final_heights.append(test_model.get_pile_height())
    print("Expected: 53.9, measured: %.2f" % np.average(final_heights))
# test_12()
