#!/usr/bin/env python
# -*- coding: utf-8 -*-

from recsys.algorithm.baseclass import Algorithm,MatrixAlgorithm
from divisi2.sparse import SparseVector
from recsys.datamodel.matrix import SparseMatrix
import math
from divisi2.sparse import SparseMatrix as divisiSparseMatrix

class ItemBased(Algorithm):

    def __init__(self, filename=None):
        super(ItemBased, self).__init__()
        self._matrix_similarity = SparseMatrix()
        self.itemTop = {}
        self.userTop = {}

    def compute(self, num=50):
        super(ItemBased, self).compute()
        userdict = self.get_data().groupbykey(isrow = False)
        itemset = list(self.get_data().get_rows())
        itemset.sort()
        itemsimilarity_matrix = divisiSparseMatrix((len(itemset),len(itemset)),row_labels=itemset,col_labels=itemset)
        for user in userdict:
            lst = userdict.get(user,[])
            for item1,value1 in lst:
                for item2,value2 in lst:
                    orgsim = itemsimilarity_matrix.entry_named(item1,item2)
                    simvalue = 1 - math.fabs(value1 - value2)
                    simvalue = min(1,max(simvalue,0))
                    itemsimilarity_matrix.set_entry_named(item1,item2,simvalue + orgsim)
        self.itemTop = {}
        for item in itemsimilarity_matrix.row_labels():
            vector = itemsimilarity_matrix.row_named(item).items()
            vector.sort(key = lambda x:x[1],reverse=True)
            self.itemTop[item] = vector[:num]
        self.userTop = {}
        for user in userdict:
            vector = []
            lst = userdict.get(user,[])
            for item in lst:
                itemlst = self.itemTop.get(item[0])
                itemlst = [[item,value * item[1]] for item, value in itemlst]
                vector.extend(itemlst)
            vector.sort(key = lambda x:x[1],reverse=True)
            self.userTop[user] = vector[:num]

    def recommend(self,i,is_row=True):
        if is_row:
            return self.itemTop.get(i,[])
        else:
            return self.userTop.get(i,[])











