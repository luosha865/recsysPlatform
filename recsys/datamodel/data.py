#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import codecs
from numpy.random import shuffle

class Data(object):
    def __init__(self):
        self._data = list([])
        self._user2extra= {}
        self._item2extra = {}

    def __repr__(self):
        s = '%d rows.' % len(self.get())
        if len(self.get()):
            s += '\nE.g: %s' % str(self.get()[0])
        return s


    def __len__(self):
        return len(self.get())

    def __getitem__(self, i):
        if i < len(self._data):
            return self._data[i]
        return None

    def get_cols(self):
        cols = set()
        for value, row, col in self.get():
            cols.add(col)
        return cols

    def get_rows(self):
        rows = set()
        for value, row, col in self.get():
            rows.add(row)
        return rows

    def normalized(self):
        valuelst = [value for value, row, col in self.get()]
        maxvalue = float(max(valuelst))
        data = [ (value/maxvalue , row,col) for value, row, col in self.get()]
        self.set(data)

    def groupbykey(self,isrow = True):
        groupdict = {}
        if isrow:
            for value, row, col in self.get():
                dict = groupdict.get(row,[])
                dict.append([col,value])
                groupdict[row] = dict
        else:
            for value, row, col in self.get():
                dict = groupdict.get(col,[])
                dict.append([row,value])
                groupdict[col] = dict

        return groupdict

    def get(self):
        return self._data

    def set(self, data, extend=False):
        if extend:
            self._data.extend(data)
        else:
            self._data = data

    def split_train_test(self, percent=80, shuffle_data=True):
        if shuffle_data:
            shuffle(self._data)
        length = len(self._data)
        train_list = self._data[:int(round(length*percent/100.0))]
        test_list = self._data[-int(round(length*(100-percent)/100.0)):]
        train = Data()
        train.set(train_list)
        test = Data()
        test.set(test_list)
        return train, test

    def crossover_split(self):
        pass

    def add_tuple(self,tuple):
        if not len(tuple) == 3:
            raise ValueError('Tuple format not correct (should be: <value, row_id, col_id>)') #value,item,user
        value, row_id, col_id = tuple
        if not value and value != 0:
            raise ValueError('Value is empty %s' % (tuple,))
        if isinstance(value, basestring):
            raise ValueError('Value %s is a string (must be an int or float) %s' % (value, tuple,))
        if row_id is None or row_id == '':
            raise ValueError('Row id is empty %s' % (tuple,))
        if col_id is None or col_id == '':
            raise ValueError('Col id is empty %s' % (tuple,))
        self._data.append(tuple)

    def load_file(self,path,sep='\t',format=None):
        linenum = 0
        for line in codecs.open(path, 'r', 'utf8'):
            linenum = linenum + 1
            data = line.strip('\r\n').split(sep)
            if not format:
                if len(data) == 3:
                    value, row_id, col_id = data
                elif len(data) == 2:
                    row_id, col_id = data
                else:
                    pass
            else:
                if format.has_key('value'):
                    value = data[format['value']]
                else:
                    value = 1
                if format.has_key('row'):
                    row_id = data[format['row']]
                else:
                    row_id = data[1]
                if format.has_key('col'):
                    col_id = data[format['col']]
                else:
                    col_id = data[2]
                if format.has_key('ids') and (format['ids'] == int or format['ids'] == 'int'):
                    try:
                        row_id = int(row_id)
                        col_id = int(col_id)
                    except Exception,e:
                        print "Error ids is not id for line %d with data %s" % (linenum,line)
            # Try to convert ids to int
            try:
                row_id = int(row_id)
            except: pass
            try:
                col_id = int(col_id)
            except: pass
            self.add_tuple((float(value), row_id, col_id))


    def sample(self,alpha=0.8):
        shuffle(self._data)
        length = len(self._data)
        sampleData = Data()
        sampleData.set(self._data[:int(round(length*alpha/100.0))])
        return sampleData


