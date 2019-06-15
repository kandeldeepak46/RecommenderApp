
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
print("Yo")



def similar_recommendation(model, interaction_matrix, user_id, user_dikt, 
                               item_dikt,threshold = 0,number_rec_items = 15):
    client=pymongo.MongoClient('mongodb://110.34.31.28:27017/')
    mydb=client['majorProject']
    mycol=mydb['bookDataset']
    #Function to produce user recommendations
    try:
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

    #     jsonScores = json.dumps(scores)
    #     print(jsonScores)

    #     return json.dumps(scores)
        client=pymongo.MongoClient('mongodb://110.34.31.28:27017/')
        mydb=client['majorProject']
        mycol=mydb['bookDataset']
        w=mycol.aggregate([{"$match":{"ISBN":{"$in":scores1}}},
                     {"$project":{'_id':0,'ISBN':'$ISBN','bookTitle':'$Book-Title','bookAuthor':'$Book-Author','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
        y=list(w)
    except:
        w=mycol.aggregate([{"$match":{"average_rating":{"$gt":4}}},{"$sample":{"size":15}},
                          {"$project":{'_id':0,'ISBN':'$ISBN','bookTitle':'$Book-Title','bookAuthor':'$Book-Author','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
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


y = similar_recommendation(model_pickle, user_item_matrix_pickle, 288858 , user_dikt_pickle, item_dikt_pickle,threshold = 7)

z = json.dumps(y)

rec_books = json.loads(z)


def get_clicks_rating(n):
    return 5*(1-0.5**n)

def get_review_rating(in_text):
    return 3

def get_net_rating(review_rating,rating,clicks_rating):
    weight=0
    weighted_rating=0
    if review_rating!=0:
        weight=weight+1
        weighted_rating=weighted_rating+review_rating
    if rating!=0:
        weight=weight+0.75
        weighted_rating=weighted_rating+rating*0.75
    if clicks_rating!=0:
        weight=weight+0.25
        weighted_rating=weighted_rating+clicks_rating*0.25
    return weighted_rating/weight


