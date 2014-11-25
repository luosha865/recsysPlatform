#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import divisi2
from numpy import loads, mean, sum, nan
from operator import itemgetter

from recsys.datamodel.matrix import SimilarityMatrix
from recsys.algorithm.baseclass import MatrixAlgorithm

class SVD(MatrixAlgorithm):

    def __init__(self, filename=None):
        super(SVD, self).__init__()
        self._U, self._S, self._V = (None, None, None)
        self._shifts = None
        self._matrix_reconstructed = None
        self._matrix_similarity = SimilarityMatrix()
        self._file_row_ids = None
        self._file_col_ids = None

    def __repr__(self):
        try:
            s = '\n'.join(('M\':' + str(self._reconstruct_matrix(force = False)), \
                'A row (U):' + str(self._reconstruct_matrix(force = False).right[1]), \
                'A col (V):' + str(self._reconstruct_matrix(force = False).left[1])))
        except TypeError:
            s = self._data.__repr__()
        return s

    def _reconstruct_similarity(self, post_normalize=True, force=True):
        if not self.get_matrix_similarity() or force:
            self._matrix_similarity = SimilarityMatrix()
            self._matrix_similarity.create(self._U, self._S, post_normalize=post_normalize)
        return self._matrix_similarity

    def _reconstruct_matrix(self, shifts=None, force=True):
        if not self._matrix_reconstructed or force:
            if shifts:
                self._matrix_reconstructed = divisi2.reconstruct(self._U, self._S, self._V, shifts=shifts)
            else:
                self._matrix_reconstructed = divisi2.reconstruct(self._U, self._S, self._V)
        return self._matrix_reconstructed

    def compute(self, k=100, cut_values=None, pre_normalize=None, mean_center=False, post_normalize=True):
        super(SVD, self).compute()
        matrix = self.preprocess(cut_values = cut_values, pre_normalize=pre_normalize, mean_center=mean_center)
        self._U, self._S, self._V = matrix.svd(k)
        self._reconstruct_similarity(post_normalize=post_normalize, force=True)
        self._reconstruct_matrix(shifts=self._shifts, force=True)

    def _get_row_reconstructed(self, i, zeros=None):
        if zeros:
            return self._matrix_reconstructed.row_named(i)[zeros]
        return self._matrix_reconstructed.row_named(i)

    def _get_col_reconstructed(self, j, zeros=None):
        if zeros:
            return self._matrix_reconstructed.col_named(j)[zeros]
        return self._matrix_reconstructed.col_named(j)

    def predict(self, i, j, MIN_VALUE=None, MAX_VALUE=None):
        if not self._matrix_reconstructed:
            self.compute() #will use default values!
        try:
            predicted_value = self._matrix_reconstructed.entry_named(i, j) #M' = U S V^t
        except IndexError,e:
            raise IndexError("user %s or item %s does not appear in train set" % (i,j))
        if MIN_VALUE:
            predicted_value = max(predicted_value, MIN_VALUE)
        if MAX_VALUE:
            predicted_value = min(predicted_value, MAX_VALUE)
        return float(predicted_value)

    def recommend(self, i, n=10, only_unknowns=False, is_row=True):
        if not self._matrix_reconstructed:
            self.compute() #will use default values!
        item = None
        zeros = []
        if only_unknowns and not self._matrix.get():
            raise ValueError("Matrix is empty! If you loaded an SVD model you can't use only_unknowns=True, unless svd.create_matrix() is called")
        if is_row:
            if only_unknowns:
                zeros = self._matrix.get().row_named(i).zero_entries()
            item = self._get_row_reconstructed(i, zeros)
        else:
            if only_unknowns:
                zeros = self._matrix.get().col_named(i).zero_entries()
            item = self._get_col_reconstructed(i, zeros)
        return item.top_items(n)
