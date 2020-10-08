import argparse

import pytest
from pytest_mock.plugin import MockFixture


def argparsing(argument: tuple) -> argparse.Namespace:
    """WARNING: This code is copy from wikipedia_sorts.py,
                so if it is updated then this function is injustice."""

    parser = argparse.ArgumentParser(description='You can try all sorting algorithm found on wikipedia.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--visualize', choices=('play', 'mp4', 'html'))
    group.add_argument('--performance', action='store_true')
    parser.add_argument('algorithm', default='all')
    parser.add_argument('target', default='random', choices=(
        'random', 'sorted', 'reversed', 'almost-sorted', 'sorted-roughly', 'few-unique'))
    parser.add_argument('size', type=int, default=32)
    parser.add_argument('--outfile', default='result')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--interval', type=int)
    group.add_argument('--fps', type=int)
    args = parser.parse_args(argument)
    return args


@pytest.mark.parametrize('test_input', 'expected', [
    (('--visualize', 'play'), (('visualize', 'play'),)),
    (('--visualize', 'mp4'), (('visualize', 'mp4'),)),
    (('--visualize', 'html'), (('visualize', 'html'),)),
    (('-v', 'play'), (('visualize', 'play'),)),
    (('-v', 'play', 'all'), (('visualize', 'play'), ('algorithm', 'all'))),
    (('-v', 'play', 'Shellsort'), (('visualize', 'play'), ('algorithm', 'Shellsort'))),
    (('-v', 'play', 'Bubble_sort'), (('visualize', 'play'), ('algorithm', 'Bubble_sort'))),
    (('-v', 'play', 'Bubble_sort;optimized'), (('visualize', 'play'), ('algorithm', 'Bubble_sort;optimized'))),
    (('-v', 'play', 'foo'), (('visualize', 'play'), ('algorithm', 'foo'))),
    (('-v', 'play', 'foo'), (('visualize', 'play'), ('algorithm', 'foo'))),
    (('-v', 'play', 'foo', 'random'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'random'))),
    (('-v', 'play', 'foo', 'sorted'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'sorted'))),
    (('-v', 'play', 'foo', 'sorted', '32'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'sorted'), ('size', 32))),
    (('-v', 'play', 'foo', 'sorted', '4'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'sorted'), ('size', 4))),
    (('-v', 'play', 'foo', 'sorted', '4', '--outfile', 'result'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'sorted'), ('size', 4), ('outfile', 'result'))),
    (('-v', 'play', 'foo', 'sorted', '4', '--outfile', 'outfile'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'sorted'), ('size', 4), ('outfile', 'outfile'))),
    (('-v', 'play', 'foo', 'sorted', '4', '--outfile', '出力ファイル'), (('visualize', 'play'), ('algorithm', 'foo'), ('target', 'sorted'), ('size', 4), ('outfile', '出力ファイル'))),
    (('-v', 'play', '--outfile', 'outfile'), (('visualize', 'play'), ('outfile', 'outfile'))),
    (('-v', 'play', '--outfile', 'outfile', '--interval', '100'), (('visualize', 'play'), ('outfile', 'outfile'), ('interval', 100))),
    (('-v', 'play', '--interval', '100'), (('visualize', 'play'), ('interval', 100))),
    (('-v', 'play', '--interval', '5'), (('visualize', 'play'), ('interval', 5))),
    (('-v', 'play', '--fps', '10'), (('visualize', 'play'), ('fps', 10))),
    (('-v', 'play', '--fps', '240'), (('visualize', 'play'), ('fps', 240))),
])
def test_argparse(test_input, expected):
    args = argparsing(test_input)
    for n, v in expected:
        assert getattr(args, n) == v


@pytest.mark.parametrize('test_input', [
    ('',),
    ('-h',),
    ('--visualize',),
    ('--visualize', 'bar'),
    ('-v', 'bar'),
    ('-v', 'play', 'foo', 'sorted', 2.71828),
    ('-v', 'play', 'foo', 'sorted', 'bar'),
    ('-v', 'play', '--interval', 'number'),
    ('-v', 'play', '--fps', 'number'),
])
def test_invalid_args(mocker: MockFixture, test_input) -> None:
    mocker.patch('argparse.ArgumentParser.exit').side_effect = Exception('testException')

    with pytest.raises(Exception) as e:
        argparsing(test_input)

    assert e.value.args[0] == 'testException'
