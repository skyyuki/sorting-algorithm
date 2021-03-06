from time import perf_counter as time
from typing import List

from utils import ChartElement, VisualSortReturn


def insertion_sort(target: List[ChartElement]) -> VisualSortReturn:
    a = target[:]
    start_time = time()
    info = {"time": 0.0,
            'comparisons': 0,
            'reads': 0,
            'writes': 0}
    frames = [(target, info.copy())]
    for i in range(len(a)):
        info['time'] = time() - start_time
        frames.append((a[:], info.copy()))
        frames[-1][0][i] = a[i].put_color('r')
        for j in range(i, 0, -1):
            info['comparisons'] += 1
            info['reads'] += 2
            if a[j] < a[j-1]:
                a[j-1], a[j] = a[j], a[j-1]
                info['writes'] += 2
                info['time'] = time() - start_time
                frames.append((a[:], info.copy()))
            else:
                break
    info['time'] = time() - start_time
    frames.append((a, info))
    return frames
