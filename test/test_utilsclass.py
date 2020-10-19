import pytest

from utils import ChartElement


@pytest.mark.parametrize('a, b, expected', [
    (ChartElement(0), ChartElement(0), '='),
    (ChartElement(6), ChartElement(6), '='),
    (ChartElement(0), ChartElement(3), '<'),
    (ChartElement(-1), ChartElement(-3), '>'),
    (ChartElement(0.5), ChartElement(0.5), '=')
])
def test_chart_element(a, b, expected):
    assert (a == b) == (expected == '=')
    assert (a != b) == (expected != '=')
    assert (a < b) == (expected == '<')
    assert (a <= b) == (expected == '<' or expected == '=')
    assert (a > b) == (expected == '>')
    assert (a >= b) == (expected == '>' or expected == '=')
