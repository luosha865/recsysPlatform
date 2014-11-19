#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
from numpy import nan


class Evaluation(object):
    def __init__(self, data=None):
        #data is a list of tuples. E.g: [(3, 2.3), (1, 0.9), (5, 4.9), (2, 0.9), (3, 1.5)]
        if data:
            self._ground_truth, self._test = map(itemgetter(0), data), map(itemgetter(1), data)
        else:
            self._ground_truth = []
            self._test = []

    def __repr__(self):
        gt = str(self._ground_truth)
        test = str(self._test)
        return 'GT  : %s\nTest: %s' % (gt, test)

    def compute(self):
        if len(self._ground_truth) == 0:
            raise ValueError('Ground Truth dataset is empty!')
        if len(self._test) == 0:
            raise ValueError('Test dataset is empty!')