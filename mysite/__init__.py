
import pandas as pd
import numpy as np
from sklearn import preprocessing
from lightfm import LightFM
# import seaborn as sns
# import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix 
from scipy.sparse import coo_matrix 
import time
from datetime import datetime, timedelta
from sklearn.metrics import roc_auc_score
from lightfm.evaluation import auc_score
import pickle
import re
import pymongo

import json

import time
from datetime import datetime


init = 'youtube'

myclient=pymongo.MongoClient('mongodb://localhost:27017/')
mydb=myclient['majorProject']
mycol=mydb['bookDataset']



def similar_recommendation(model, interaction_matrix, user_id, user_dikt, 
                               item_dikt,threshold = 0,number_rec_items = 15):
    myclient=pymongo.MongoClient('mongodb://localhost:27017/')
    mydb=myclient['majorProject']
    mycol=mydb['bookDataset']
    #Function to produce user recommendations

    # x=mydb['userActivity'].aggregate([{"$match":{"isFifteen":0}},{"$addFields":{"size":{"$size":"$activity"}}},{"$match":{"size":{"$gt":0}}},{"$project":{"user_id":1,"_id":0,"activity":{"book_id":1,"activity":{"net_rating":1}}}},{"$unwind":"$activity"},{"$project":{"user_id":1,"activity":"$activity.book_id","rating":"$activity.activity.net_rating"}}]);
    # y=mydb['userActivity'].aggregate([{"$match":{"isFifteen":0}},{"$addFields":{"size":{"$size":"$activity"}}},{"$match":{"size":{"$gt":0}}},{"$project":{"user_id":1,"_id":0}}]);
    # userlist=list(y)
    # interaction_data=list(x)

    # for i in range (len(userlist)):
    #     mycol.update({"user_id":userlist[i]['user_id']},{"$set":{"isFifteen":1 }})

    # for i in range(len(interaction_data)):
    #     user_item_matrix_pickle[interaction_data[i]['activity']][int(userlist[i]['user_id'])] =int(interaction_data[i]['rating'])



    x=mycol.find({"user_id":user_id,"isFifteen":1})
    isFifteen=x.count()
    print('------------------------------------------isFifteen---------------------------')
    print(isFifteen)

    try:
        print("-------------------15 books------------------------------")
        n_users, n_items = interaction_matrix.shape
        user_x = user_dikt[user_id]
        scores = pd.Series(model.predict(user_x,np.arange(n_items)))
        scores.index = interaction_matrix.columns
        scores = list(pd.Series(scores.sort_values(ascending=False).index))

        known_items = list(pd.Series(interaction_matrix.loc[user_id,:][interaction_matrix.loc[user_id,:] > threshold].index).sort_values(ascending=False))

        scores = [x for x in scores if x not in known_items]
        print(len(scores))
        score_list = scores[0:number_rec_items]

        known_items = list(pd.Series(known_items).apply(lambda x: item_dikt[x]))
        scores = list(pd.Series(score_list).apply(lambda x: item_dikt[x]))
        scores1 = list(pd.Series(score_list))

        w=mycol.aggregate([{"$match":{"ISBN":{"$in":scores1}}},
                     {"$project":{'_id':0,'ISBN':'$ISBN', 'bookTitle':'$Book-Title','bookAuthor':'$Book-Author','genres':'$genres','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
        y=list(w)
    except:
        w=mycol.aggregate([{"$match":{"average_rating":{"$gt":4}}},{"$sample":{"size":15}},
                          {"$project":{'_id':0,'ISBN':'$ISBN','bookTitle':'$Book-Title','bookAuthor':'$Book-Author','genres':'$genres','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
        y=list(w)
    
    return y


with open('model.pickle', 'rb') as handle:
    model_pickle = pickle.load(handle)

with open('item_dikt.pickle', 'rb') as handle:
   item_dikt_pickle = pickle.load(handle)

with open('user_item_matrix.pickle', 'rb') as handle:
    user_item_matrix_pickle = pickle.load(handle)

with open('user_dikt.pickle', 'rb') as handle:
    user_dikt_pickle = pickle.load(handle)




def get_clicks_rating(n):
    return 5*(1-0.5**n)

def get_review_rating(in_text):
    return 3

def get_net_rating(review_rating,rating,clicks_rating):
    print("------------------------------get_net_rating-------------------------------")
    
    review_rating = float(review_rating)
    rating = float(rating)
    clicks_rating = float(clicks_rating)
    weight=0
    weighted_rating=0
    if review_rating!=0:
        weight=weight+1
        weighted_rating=weighted_rating+review_rating
    if rating!=0:
        weight=weight+0.8
        weighted_rating=weighted_rating+rating*0.8
    if clicks_rating!=0:
        weight=weight+0.2
        weighted_rating=weighted_rating+clicks_rating*0.2
    net_rating = weighted_rating/weight
    return net_rating
    # return 5


def get_recommendation(userId):
    y = similar_recommendation(model_pickle, user_item_matrix_pickle, 125 , user_dikt_pickle, item_dikt_pickle,threshold = 7)
    z = json.dumps(y)
    rec_books = json.loads(z)
    return rec_books