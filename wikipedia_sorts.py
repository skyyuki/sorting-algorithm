import argparse
import math
import random
from typing import List, Callable

from matplotlib import pyplot as plt, animation


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


def get_visual_sorter(algorithm_name: str) -> Callable:
    pass


def draw_charts(algorithms: List[str], target_set: List[int], interval: int) -> animation.FuncAnimation:
    # Setup draw area
    fig = plt.figure(1)
    axs = []

    square_side_float, square_side_int = math.modf(math.sqrt(len(algorithms)))
    if square_side_float == 0:
        rows, cols = square_side_int, square_side_int
    elif square_side_float > 0.5:
        rows, cols = square_side_int+1, square_side_int+1
    else:
        rows, cols = square_side_int+1, square_side_int
    for i in range(len(algorithms)):
        axs.append(fig.add_subplot(rows, cols, i+1))

    # Get frames
    target_set = list(map(int, target_set))
    frames = []
    if 'all' in algorithms:
        algorithms = []
    for algorithm in algorithms:
        frames.append(get_visual_sorter(algorithm)(target_set))
    # frames = [get_sorter(algorithm) for algorithm in algorithms]
    frames = zip(frames)

    def animate(frame):
        # bars = []
        for i, (array, info) in enumerate(frame):
            axs[i].cla()
            axs[i].set_titile(algorithms[i])
            axs[i].set_xticks([])
            axs[i].set_yticks([])
            axs[i].bar(range(args.size), 
                       array)
        # return bars

    # Animation
    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval)
    return anim


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
    group.add_argument('--interval', default=100, type=int)
    group.add_argument('--fps', default=25, type=int)
    args = parser.parse_args()

    target = generate_target(args.target, args.size)

    if args.visualize:
        draw_charts(args.algorithm, target, args.interval)
