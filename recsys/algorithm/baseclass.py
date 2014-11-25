#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from scipy.cluster.vq import kmeans2 #for kmeans method
from random import randint #for kmeans++ (_kinit method)
#from scipy.linalg import norm #for kmeans++ (_kinit method)
from scipy import array #for kmeans method
from numpy import sum
from numpy.linalg import norm #for _cosine and kmeans++ (_kinit method)
from csc import divisi2
from recsys.datamodel.data import Data
from recsys.datamodel.matrix import SparseMatrix

class Algorithm(object):
    def __init__(self):
        self._data = Data()

    def __repr__(self):
        s = '%d rows.' % len(self.get_data())
        if len(self.get_data()):
            s += '\nE.g: %s' % str(self.get_data()[0])
        return s

    def __len__(self):
        return len(self.get_data())

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def add_tuple(self, tuple):
        self.get_data().add_tuple(tuple)

    def load_data(self, filename, sep='\t', format={'value':0, 'row':1, 'col':2}):
        self._data.load_file(filename, sep, format)

    def compute(self):
        if not self._data.get():
            raise ValueError('No data set. Matrix is empty!')




class MatrixAlgorithm(Algorithm):
    def __init__(self):
        super(MatrixAlgorithm, self).__init__()
        self._matrix = SparseMatrix()
        self._matrix_similarity = None #self-similarity matrix (only for the input Matrix rows)
        self._matrix_and_data_aligned = False #both Matrix and Data contain the same info?

    def get_matrix(self):
        if not self._matrix.get():
            self.create_matrix()
        return self._matrix

    def get_matrix_similarity(self):
        return self._matrix_similarity

    def set_data(self, data):
        self._data = data
        self._matrix_and_data_aligned = False

    def add_tuple(self, tuple):
        self.get_data().add_tuple(tuple)
        self._matrix_and_data_aligned = False

    def create_matrix(self):
        #try:
        self._matrix.create(self._data.get())
        #except AttributeError:
        #self._matrix.create(self._data)
        self._matrix_and_data_aligned = True

    def predict(self, i, j, MIN_VALUE=None, MAX_VALUE=None):
        raise NotImplementedError("cannot instantiate Abstract Base Class")

    def recommend(self, i, n=10):
        raise NotImplementedError("cannot instantiate Abstract Base Class")


    def compute(self):
        if self._matrix.empty() and (not isinstance(self._data, list) and not self._data.get()):
            raise ValueError('No data set. Matrix is empty!')
        if self._matrix.empty() and (isinstance(self._data, list) and not self._data):
            raise ValueError('No data set. Matrix is empty!')
        if not self._matrix.empty() or not self._matrix_and_data_aligned:
            self.create_matrix()

    def preprocess(self, cut_values=None,pre_normalize=None, mean_center=False):
        if cut_values:
            self._matrix.set(self._matrix.get().squish(cut_values))

        matrix = self._matrix.get()

        if mean_center:
            matrix, row_shift, col_shift, total_shift = matrix.mean_center()
            self._shifts = (row_shift, col_shift, total_shift)

        if pre_normalize:
            if pre_normalize == 'tfidf':
                matrix = matrix.normalize_tfidf()
            elif pre_normalize == 'rows':
                matrix = matrix.normalize_rows()
            elif pre_normalize == 'cols':
                matrix = matrix.normalize_cols()
            elif pre_normalize == 'all':
                matrix = matrix.normalize_all()
            else:
                raise ValueError("Pre-normalize option (%s) is not correct.\n \
                                  Possible values are: 'tfidf', 'rows', 'cols' or 'all'" % pre_normalize)
        return matrix

    def _get_row_similarity(self, i):
        if not self.get_matrix_similarity() or self.get_matrix_similarity().get() is None:
            self.compute()
        try:
            return self.get_matrix_similarity().get_row(i)
        except KeyError:
            raise KeyError("%s not found!" % i)

    def similar(self, i, n=10):
        if not self.get_matrix_similarity() or self.get_matrix_similarity().get() is None:
            self.compute()
        return self._get_row_similarity(i).top_items(n)

    def similarity(self, i, j):
        if not self.get_matrix_similarity() or self.get_matrix_similarity().get() is None:
            self.compute()
        return self.get_matrix_similarity().value(i, j)

