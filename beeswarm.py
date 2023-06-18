import numpy as np
import pandas as pd

class _Intervals:
    def __init__(self, *intervals) -> None:
        intervals_ = []
        for interval in intervals:
            if isinstance(interval, pd.Interval):
                intervals_.append(interval)
            else:
                intervals_.append(pd.Interval(*interval, 'both'))
        intervals_.sort()
        self.intervals, self.array = self._collate_intervals(np.array(intervals_))

    @staticmethod
    def _get_overlaps(ints1, ints2):
        overlap_mat = np.zeros((len(ints1), len(ints2)), dtype=bool)
        for i, int1 in enumerate(ints1):
            for j, int2 in enumerate(ints2):
                overlap_mat[i, j] = int1.overlaps(int2)
        return overlap_mat

    @staticmethod
    def _get_array(intervals):
        interval_array = []
        for interval in intervals:
            interval_array.append([interval.left, interval.right])
        return np.array(interval_array)  

    def _collate_intervals(self, intervals):
        overlap_mat = self._get_overlaps(intervals, intervals)
        array = self._get_array(intervals)
        mat_shape_prev = tuple()
        mat_shape = overlap_mat.shape
        while mat_shape_prev != mat_shape:
            mat_shape_prev = mat_shape
            collate_idxs = overlap_mat[overlap_mat.sum(0).argmax()]
            collated = array[collate_idxs]
            collated_interval = pd.Interval(collated.min(), collated.max(), 'both')
            intervals = np.append(intervals[~collate_idxs], collated_interval)
            intervals.sort()
            overlap_mat = self._get_overlaps(intervals, intervals)
            array = self._get_array(intervals)
            mat_shape = overlap_mat.shape
        return intervals, array

    def __and__(self, intervals):
        if not isinstance(intervals, _Intervals):
            raise RuntimeError('& on Intervals is compatible to only Intervals')
        intervals = np.concatenate([self.intervals, intervals.intervals])
        return _Intervals(*self._collate_intervals(intervals)[0])

def swarm(x0, ys, r):
    ys = np.sort(np.asarray(ys).squeeze())
    if ys.ndim != 1: raise RuntimeError('input values must be 1-d')
    points = []
    for i, y in enumerate(ys):
        if i == 0:
            x = x0
        else:
            dy = y - np.array(points)[:, 1, np.newaxis]
            if (window := dy <= 2 * r).sum():
                dy_w = dy[window, np.newaxis]
                dx_w = np.sqrt(4 * r ** 2 - dy_w ** 2)
                x_iw = np.array(points)[window.reshape(-1)][:, 0, np.newaxis]
                intervals = _Intervals(*np.concatenate([x_iw - dx_w, x_iw + dx_w], 
                                                      axis=-1))
                x0_in_interval = any(x0 in interval for interval 
                                        in intervals.intervals)
                if x0_in_interval:
                    proximity = np.abs(intervals.array - x0)
                    x = intervals.array[np.where(proximity == proximity.min())][0]
                else: x = x0
            else: x = x0
        points.append(np.array([x, y]))
    return np.array(points)



'''
import numpy as np
from beeswarm.beeswarm import *
xy = swarm(0, np.random.uniform(0, 15, 30), 1)
from bokeh.plotting import figure, show
plot = figure(height=500, width=500, x_range=(-9, 9), y_range=(-1, 17))
plot.scatter(x=xy[:, 0], y=xy[:, 1], marker='circle', radius=1, fill_alpha=0.1)
show(plot)
'''