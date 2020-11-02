import importlib
import random

import pytest

from utils import ChartElement

sub_sorters = {'insertion_sort': ('insertion_sort',)}
random.seed(1)
origin = list(map(ChartElement, range(1000)))


@pytest.fixture
def sorter(request):
    module = importlib.import_module('visual_sorting.' + request.param)
    return [getattr(module, func_name) for func_name in sub_sorters[request.param]]


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
    choices(origin, 1000),
], ids=['sorted', 'reversed', 'shuffle01', 'shuffle02', 'shuffle03', 'choices01', 'choices02', 'choices03'])
@pytest.mark.parametrize('sorter', sub_sorters, indirect=['sorter'])
def test_sorting(sorter, target, expected):
    for sorter in sorter:
        assert sorter(target[:])[-1][0] == expected
