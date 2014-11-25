#!/usr/bin/env python
#-*- coding: utf-8 -*-

from recsys.algorithm.svd import SVD
from recsys.algorithm.itembased import ItemBased
from recsys.datamodel.data import Data
from recsys.evaluation.rmse import RMSE

#col is user , row is item

def test_svd(train,test,data):
    svd = SVD()
    svd.set_data(train)
    print svd

    k = 100
    svd.compute(k=k,
                cut_values=10,
                pre_normalize=None,
                mean_center=True,
                post_normalize=True)
    print svd

    MIN_RATING = 0.0
    MAX_RATING = 5.0
    ITEMID = 1
    USERID = 1

    #print svd.predict(ITEMID, USERID, MIN_RATING, MAX_RATING)
    print svd.recommend(USERID, is_row=False) #cols are users and rows are items, thus we set is_row=False
    print svd.recommend(ITEMID)

    r_info = []
    for rate,user,item in test.get():
        try:
            pred_rate = svd.predict(user,item)
            r_info.append((rate,pred_rate))
        except IndexError,e:
            pass

    print test
    print len(r_info),r_info[1:10]

    value = RMSE(r_info).compute()
    print value





def test_itembased(train,test,data):
    itembased = ItemBased()
    itembased.set_data(train)
    itembased.compute(num = 100)
    ITEMID = 1
    USERID = 1
    #print svd.predict(ITEMID, USERID, MIN_RATING, MAX_RATING)
    print itembased.recommend(USERID, is_row=False) #cols are users and rows are items, thus we set is_row=False
    print itembased.recommend(ITEMID)


data = Data()
data.load_file(path='../../data/ratings.dat',sep='::'
          , format={'col':0, 'row':1,'value':2, 'ids': int})
print len(data.get())
train,test = data.split_train_test(percent = 100)
#test_svd(train,test,data)
test_itembased(train,test,data)



