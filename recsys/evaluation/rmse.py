#!/usr/bin/env python
# -*- coding: utf-8 -*-

from recsys.evaluation.baseclass import Evaluation
from recsys.evaluation import ROUND_FLOAT
from math import sqrt

class RMSE(Evaluation):
    def __init__(self, data=None):
        super(RMSE, self).__init__(data)

    def compute(self, r=None, r_pred=None):
        if r and r_pred:
            return round(sqrt(abs((r - r_pred)*(r - r_pred))), ROUND_FLOAT)

        if not len(self._ground_truth) == len(self._test):
            raise ValueError('Ground truth and Test datasets have different sizes!')

        #Compute for the whole test set
        super(RMSE, self).compute()
        sum = 0.0
        for i in range(0, len(self._ground_truth)):
            r = self._ground_truth[i]
            r_pred = self._test[i]
            sum += abs((r - r_pred)*(r - r_pred))
        return round(sqrt(abs(float(sum/len(self._test)))), ROUND_FLOAT)