import argparse


if __name__ == '__main__':
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
    args = parser.parse_args()
