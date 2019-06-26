
import pandas as pd
import numpy as np
from sklearn import preprocessing
from lightfm import LightFM
# import seaborn as sns
# import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix 
from scipy.sparse import coo_matrix 
import scipy
import time
from datetime import datetime, timedelta
from sklearn.metrics import roc_auc_score
from lightfm.evaluation import auc_score
import pickle
import re
import pymongo


import json

import time
from apscheduler.schedulers.background import BackgroundScheduler

import datetime


REFRESH_INTERVAL = 60 #seconds
 
scheduler = BackgroundScheduler()
scheduler.start()


init = 'youtube'

myclient=pymongo.MongoClient('mongodb://localhost:27017/')
mydb=myclient['majorProject']
mycol=mydb['bookDataset']


def get_recommendation(userId):
    y, heading = similar_recommendation(model_pickle, user_item_matrix_pickle, userId , user_dikt_pickle,threshold = 7)
    z = json.dumps(y)
    rec_books = json.loads(z)
    return rec_books, heading


def similar_recommendation(model, interaction_matrix, user_id, user_dikt, 
                               threshold = 0,number_rec_items = 15):
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

    print(user_id)

    x=mydb['userActivity'].find({"user_id":user_id,"isFifteen":1})
    isFifteen=x.count()
    print('------------------------------------------isFifteen---------------------------')
    
    print(isFifteen)


    if (isFifteen == 1):
        print("-------------------15 books------------------------------")
        n_users, n_items = interaction_matrix.shape
        user_x = user_dikt[user_id]
        scores = pd.Series(model.predict(user_x,np.arange(n_items)))
        scores.index = interaction_matrix.columns
        scores = list(pd.Series(scores.sort_values(ascending=False).index))

        known_items = list(pd.Series(interaction_matrix.loc[user_id,:][interaction_matrix.loc[user_id,:] > threshold].index).sort_values(ascending=False))

        scores = [x for x in scores if x not in known_items]
        # print(len(scores))
        score_list = scores[0:number_rec_items]

        # known_items = list(pd.Series(known_items).apply(lambda x: item_dikt[x]))
        # scores = list(pd.Series(score_list).apply(lambda x: item_dikt[x]))
        scores1 = list(pd.Series(score_list))

        w=mycol.aggregate([{"$match":{"ISBN":{"$in":scores1}}},
                     {"$project":{'_id':0,'ISBN':'$ISBN', 'bookTitle':'$Book-Title','bookAuthor':'$Book-Author','genres':'$genres','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
        y=list(w)
        heading = "Recommended books"

    else:
        print("--------------------------random-----------------------------------")
        w=mycol.aggregate([{"$match":{"average_rating":{"$gt":4}}},{"$sample":{"size":15}},
                          {"$project":{'_id':0,'ISBN':'$ISBN','bookTitle':'$Book-Title','bookAuthor':'$Book-Author','genres':'$genres','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
        y=list(w)
        heading = "Random books"

    return y, heading

# name="name1"


# new_name=get_new_name(name)

# get_new_name(name)
# {
#     if(name="name1")
#     {
#         new_name="name2"
#     }
#     else
#     {
#         new_name="name1"
#     }
#     return new_name

# }








def get_clicks_rating(n):
    return 5*(1-0.5**n)

def get_review_rating(in_text):
    return 3

def get_net_rating(review_rating,rating,clicks_rating):
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

    with open('model.pickle', 'rb') as handle:
        model_pickle = pickle.load(handle)

    with open('item_dikt.pickle', 'rb') as handle:
        item_dikt_pickle = pickle.load(handle)

    with open('user_item_matrix.pickle', 'rb') as handle:
        user_item_matrix_pickle = pickle.load(handle)

    with open('user_dikt.pickle', 'rb') as handle:
        user_dikt_pickle = pickle.load(handle)

    y = similar_recommendation(model_pickle, user_item_matrix_pickle, userId , user_dikt_pickle,threshold = 7)
    z = json.dumps(y)
    rec_books = json.loads(z)
    return rec_books


# this returns list of user_id from interaction matrix (row name)
# key is user_id value is matrix index
def user_item_dikts(interaction_matrix):
    user_ids = list(interaction_matrix.index)
    user_dikt = {}
    counter = 0 
    for i in user_ids:
        user_dikt[i] = counter
        counter += 1
    return user_dikt



def talkShow():
    print('---------------------------------------James Corden---------------------------------------------')
    myClient=pymongo.MongoClient("localhost:27017")
    mydb=myClient['majorProject']
    mycol=mydb['userActivity']

    # import interaction matrix file
    with open('user_item_matrix.pickle', 'rb') as handle:
        user_item_matrix_pickle = pickle.load(handle)


    # for modifying date
    x=mydb['date_modified'].find({},{"_id":0,"date_modified":1})
    last_date_modified=list(x)[0]['date_modified']
    # print(p)


    # This adds new books at the end of interaction matrix 
    # The last_date_modified needs to be updated here. Right now, the date is harcoded
    # x=mydb['bookDataset'].aggregate([{"$match":{"date_added":{"$gt":datetime.datetime(2019, 6, 21, 8, 25,50)}}},{"$project":{"_id":0,"ISBN":1}}])
    # data=list(x)
    # print(data)
    # for i in data:
    #     user_item_matrix_pickle[i['ISBN']]=0


    # For isFifteen =1 users and newly modified activity only
    x=mycol.aggregate([{"$match":{"activity.activity.date_modified":{"$lte":last_date_modified}}},{"$unwind":"$activity"},{"$match":{"isFifteen":1}},{"$match":{"activity.activity.date_modified":{"$gte":last_date_modified}}},{"$project":{"_id":0,"activity.activity.net_rating":1,"activity.activity.date_modified":1,"activity.book_id":1,"user_id":1}}])
    data=list(x)
    a=[]
    for i in range(len(data)):
        a.append({"user_id":data[i]['user_id'],"activity":data[i]['activity']['book_id'],"rating":data[i]['activity']['activity']['net_rating']})


    # obtain activity of user (isFifteen= 0 and rating>15) on book
    x=mydb['userActivity'].aggregate([{"$match":{"isFifteen":0}},{"$addFields":{"size":{"$size":"$activity"}}},{"$match":{"size":{"$gt":5}}},{"$project":{"user_id":1,"_id":0,"activity":{"book_id":1,"activity":{"net_rating":1}}}},{"$unwind":"$activity"},{"$project":{"user_id":1,"activity":"$activity.book_id","rating":"$activity.activity.net_rating"}}]);
    interaction_data=list(x)
    # obtain the list of new user to update (isFifteen =0 and rating>15)
    y=mydb['userActivity'].aggregate([{"$match":{"isFifteen":0}},{"$addFields":{"size":{"$size":"$activity"}}},{"$match":{"size":{"$gt":5}}},{"$project":{"user_id":1,"_id":0}}]);
    userlist=list(y)

    # add both users
    interaction_data=interaction_data+a


    # For isFifteen=0 users
    # this add new user to interaction matrix and initialize it to zero
    for i in range (len(userlist)):
        # this add new user to interaction matrix and initialize it to zero
        user_item_matrix_pickle.loc[int(userlist[i]['user_id'])]=0
       
    #     this update isFifteen flag value
        mycol.update({"user_id":userlist[i]['user_id']},{"$set":{"isFifteen":1 }})
        

    # updates all the new ratings
    # this loops throught all the value interaction book and update the values with respective rating
    for i in range(len(interaction_data)):
        user_item_matrix_pickle[interaction_data[i]['activity']][int(interaction_data[i]['user_id'])] =round(2*float(interaction_data[i]['rating'])) 
           
    #for modifying date
    mydb['date_modified'].update({},{"$set":{"date_modified":datetime.datetime.now()}})

    # after interaction matrix is update, this convert pandas dataframe into scipy sparse matrix
    user_item_matrix_sci = scipy.sparse.csr_matrix(user_item_matrix_pickle.values)


    user_dikt = user_item_dikts(user_item_matrix_pickle)

    model_pickle=LightFM(no_components=115,learning_rate=0.027,loss='warp')
    model_pickle.fit(user_item_matrix_sci,epochs=12,num_threads=4)


    with open('user_item_matrix.pickle', 'wb') as handle:
        pickle.dump(user_item_matrix_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('model.pickle', 'wb') as handle:
        pickle.dump(model_pickle, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('user_dikt.pickle', 'wb') as handle:
        pickle.dump(user_dikt, handle, protocol=pickle.HIGHEST_PROTOCOL)

talkShow()
scheduler.add_job(talkShow, 'interval', seconds = REFRESH_INTERVAL)

