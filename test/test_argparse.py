import argparse

import pytest
from pytest_mock.plugin import MockerFixture


def argparsing(argument: tuple) -> argparse.Namespace:
    """WARNING: This code is copy from wikipedia_sorts.py,
                so if it is updated then this function is injustice."""
    print(argument)

    parser = argparse.ArgumentParser(
        description='You can try all sorting algorithm found on wikipedia.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-v', '--visualize', choices=('play', 'mp4', 'html'))
    group.add_argument('-p', '--performance')
    parser.add_argument('-a', '--algorithm', nargs='*', default='all')
    parser.add_argument('--target', default='random', choices=(
        'random', 'sorted', 'reversed', 'almost-sorted', 'sorted-roughly', 'few-unique'))
    parser.add_argument('--size', type=int, default=32)
    parser.add_argument('-o', '--outfile', default='result')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--interval', type=int)
    group.add_argument('--fps', type=int)
    args = parser.parse_args(argument)
    return args


@pytest.mark.parametrize('test_input, expected', [
    (('--visualize', 'play'), (('visualize', 'play'),)),
    (('--visualize', 'mp4'), (('visualize', 'mp4'),)),
    (('--visualize', 'html'), (('visualize', 'html'),)),
    (('-v', 'play'), (('visualize', 'play'),)),
    (('--visualize', 'play', '--algorithm', 'all'), (('visualize', 'play'), ('algorithm', ['all']))),
    (('--visualize', 'play', '--algorithm', 'Shellsort'), (('visualize', 'play'), ('algorithm', ['Shellsort']))),
    (('--visualize', 'play', '--algorithm', 'Bubble_sort'), (('visualize', 'play'), ('algorithm', ['Bubble_sort']))),
    (('--visualize', 'play', '--algorithm', 'Bubble_sort;optimized'), (('visualize', 'play'), ('algorithm', ['Bubble_sort;optimized']))),
    (('--visualize', 'play', '--algorithm', 'Bubble_sort', 'Insertion_sort'), (('visualize', 'play'), ('algorithm', ['Bubble_sort', 'Insertion_sort']))),
    (('--visualize', 'play', '--algorithm', 'Bubble_sort;optimized', 'Insertion_sort', 'Merge_sort'), (('visualize', 'play'), ('algorithm', ['Bubble_sort;optimized', 'Insertion_sort', 'Merge_sort']))),
    (('-v', 'play', '-a', 'myalgorithm'), (('visualize', 'play'), ('algorithm', ['myalgorithm']))),
    (('--visualize', 'play', '--algorithm', 'foo'), (('visualize', 'play'), ('algorithm', ['foo']))),
    (('--visualize', 'play', '--algorithm', 'foo'), (('visualize', 'play'), ('algorithm', ['foo']))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'random'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'random'))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'sorted'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'sorted'))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'sorted', '--size', '32'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'sorted'), ('size', 32))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'sorted', '--size', '4'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'sorted'), ('size', 4))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'sorted', '--size', '4', '--outfile', 'result'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'sorted'), ('size', 4), ('outfile', 'result'))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'sorted', '--size', '4', '--outfile', 'outfile'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'sorted'), ('size', 4), ('outfile', 'outfile'))),
    (('--visualize', 'play', '--algorithm', 'foo', '--target', 'sorted', '--size', '4', '--outfile', '出力ファイル'), (('visualize', 'play'), ('algorithm', ['foo']), ('target', 'sorted'), ('size', 4), ('outfile', '出力ファイル'))),
    (('--visualize', 'play', '--outfile', 'outfile'), (('visualize', 'play'), ('outfile', 'outfile'))),
    (('-v', 'play', '-o', 'ofile'), (('visualize', 'play'), ('outfile', 'ofile'))),
    (('--visualize', 'play', '--outfile', 'outfile', '--interval', '100'), (('visualize', 'play'), ('outfile', 'outfile'), ('interval', 100))),
    (('--visualize', 'play', '--interval', '100'), (('visualize', 'play'), ('interval', 100))),
    (('--visualize', 'play', '--interval', '5'), (('visualize', 'play'), ('interval', 5))),
    (('--visualize', 'play', '--fps', '10'), (('visualize', 'play'), ('fps', 10))),
    (('--visualize', 'play', '--fps', '240'), (('visualize', 'play'), ('fps', 240))),
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
    ('--visualize', 'bar'),
    ('--visualize', 'play', '--target', 'sorted', '--size', '2.71828'),
    ('--visualize', 'play', '--target', 'sorted', '--size', 'bar'),
    ('--visualize', 'play', '--interval', 'number'),
    ('--visualize', 'play', '--fps', 'number'),
])
def test_invalid_args(mocker: MockerFixture, test_input) -> None:
    mocker.patch('argparse.ArgumentParser.exit').side_effect = Exception('testException')

    with pytest.raises(Exception) as e:
        argparsing(test_input)

    assert e.value.args[0] == 'testException'
