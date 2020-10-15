import argparse
import random
from typing import List


def generate_target(sequence: str, size: int) -> List[int]:
    target_ = list(range(1, size + 1))
    if sequence == 'random':
        random.shuffle(target_)
    elif sequence == 'sorted':
        pass
    elif sequence == 'reversed':
        target_ = list(reversed(target_))
    elif sequence == 'almost-sorted':
        target_.append(target_.pop(size // 2))
    elif sequence == 'sorted-roughly':
        # TODO: use shell_sort or comb_sort
        pass
    elif sequence == 'few-unique':
        target_ = [(1 + i // (size // 4)) * (size // 4) for i in range(size)]
        random.shuffle(target_)
    return target_


def draw_charts(algorithms: List[str], interval: int):
    pass


if __name__ == '__main__':
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
    args = parser.parse_args()
    target = generate_target(args.target, args.size)

    print(args)
