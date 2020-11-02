from time import perf_counter as time
from typing import Tuple, List, Dict, Union

from utils import ChartElement


def insertion_sort(target: List[ChartElement]) -> List[Tuple[list, Dict[str, Union[float, int]]]]:
    a = target[:]
    start_time = time()
    info = {"time": 0.0,
            'comparisons': 0,
            'reads': 0,
            'write': 0}
    frames = [(target, info)]
    for i in range(len(a)):
        info['time'] = start_time - time()
        frames.append((a, info))
        frames[-1][0][i].color = 'r'
        for j in range(i, 0, -1):
            info['comparisons'] += 1
            info['reads'] += 2
            if a[j] < a[j-1]:
                a[j-1], a[j] = a[j], a[j-1]
                info['write'] += 2
                info['time'] = start_time - time()
                frames.append((a, info))
            else:
                break
    info['time'] = start_time - time()
    frames.append((a, info))
    return frames
