import random

import pytest

from utils import ChartElement

sub_sorters = {'insertion_sort': ('insertion_sort',)}
random.seed(1)
origin = list(map(ChartElement, range(1000)))


def shuffle(array):
    array = array[:]
    random.shuffle(array)
    return array


def choices(array, size):
    array = random.choices(array, k=size)
    return array, sorted(array)


@pytest.mark.parametrize('target, expected', [
    (origin, origin),
    (list(reversed(origin)), origin),
    (shuffle(origin), origin),
    (shuffle(origin), origin),
    (shuffle(origin), origin),
    choices(origin, 1000),
    choices(origin, 1000),
], ids=['sorted', 'reversed', 'shuffle01', 'shuffle02', 'shuffle03',
        'choices01', 'choices02'])
def test_sorting(sorter, target, expected):
    # sorter is defined in conftest.py and
    # generate parameters of test in sub_sorters.
    result = sorter(target)[-1]
    assert result[0] == expected
    print(result[1])
