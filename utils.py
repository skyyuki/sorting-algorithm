
class ChartElement:
    max: int = 32

    def __init__(self, v: int):
        self._v = v
        self.color = (0,
                      0.5 - v / ChartElement.max / 2,
                      v / ChartElement.max / 2)

    def __repr__(self):
        return repr(self._v)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._v == other._v
        else:
            kls = other.__class__.__name__
            raise NotImplementedError(
                f'comparison between ChartElement and {kls} is not supported')

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self._v < other._v
        else:
            kls = other.__class__.__name__
            raise NotImplementedError(
                f'comparison between ChartElement and {kls} is not supported')

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)
