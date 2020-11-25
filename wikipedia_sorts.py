import argparse
import importlib
import math
import random
from itertools import zip_longest
from typing import List, Callable

from matplotlib import pyplot as plt, animation

from utils import ChartElement


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
    algorithm_name = algorithm_name.lower()
    module = importlib.import_module('visual_sorting.'+algorithm_name)
    return getattr(module, algorithm_name)


def draw_charts(algorithms: List[str], target_set: List[int], interval: int) -> animation.FuncAnimation:
    fig = plt.figure(1)

    # Make subplots square or rectangular to minimize wasted space
    square_side = math.sqrt(len(algorithms))
    if square_side.is_integer():
        rows, cols = int(square_side), int(square_side)
    else:
        rows, cols = round(square_side), int(square_side)+1
    axs = [fig.add_subplot(rows, cols, i + 1) for i in range(len(algorithms))]

    # Run sorts to get frames
    target_set = list(map(ChartElement, target_set))
    if 'all' in algorithms:
        algorithms = []
        # TODO: case of 'all'
    frames = tuple(zip_longest(*[get_visual_sorter(algorithm)(target_set) for algorithm in algorithms]))

    def animate(frame):
        # bars = []
        for i, (array, info) in enumerate(frame):
            axs[i].cla()
            axs[i].set_title(algorithms[i])
            axs[i].set_xticks([])
            axs[i].set_yticks([])
            axs[i].bar(range(ChartElement.max),  # x
                       [int(v) for v in array],  # y
                       1,  # width
                       color=[d.color for d in array])  # color
            axs[i].text(0, ChartElement.max,  # position
                        '\n'.join((f'{key}: {info[key]}' for key in info)),  # text
                        va='top',  # vertical alignment
                        bbox={'fc': "none"})  # box
        # return bars

    return animation.FuncAnimation(fig, animate, frames=frames, interval=interval)


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
        ChartElement.max = args.size
        anim = draw_charts(args.algorithm, target, args.interval)
        if args.visualize == 'play':
            plt.show()
        elif args.visualize == 'mp4':
            anim.save(args.outfile+'.mp4', animation.FFMpegWriter(
                args.fps, extra_args=['-vcodec', 'libx264', '-tune',
                                      'stillimage']))
        elif args.visualize == 'html':
            anim.save(args.outfile+'.html', animation.HTMLWriter(args.fps))
