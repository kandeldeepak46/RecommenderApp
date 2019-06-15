
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


init = 'youtube'
print("Yo")


def similar_recommendation(model, interaction_matrix, user_id, user_dikt, 
                               item_dikt,threshold = 0,number_rec_items = 15):

    #Function to produce user recommendations

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
    x=mycol.aggregate([{"$match":{"ISBN":{"$in":scores1}}},
                {"$project":{'_id':0,'ISBN':'$ISBN','bookTitle':'$Book-Title','bookAuthor':'$Book-Author','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} }])
    
    y=list(x)     
    print(scores1)
    print(scores)
    # new dataframe for books
    book_newdf = pd.DataFrame({'bookTitle':scores})
   
    print("Items that were liked by the User:")
    counter = 1
    for i in known_items[:25]:
        print(str(counter) + '- ' + i)
        counter+=1

    print("\n Recommended Items:")
    counter = 1
    for i in scores:
        print(str(counter) + '- ' + i)
        counter+=1
    return book_newdf,y


with open('model.pickle', 'rb') as handle:
    model_pickle = pickle.load(handle)

with open('item_dikt.pickle', 'rb') as handle:
   item_dikt_pickle = pickle.load(handle)

with open('user_item_matrix.pickle', 'rb') as handle:
    user_item_matrix_pickle = pickle.load(handle)

with open('user_dikt.pickle', 'rb') as handle:
    user_dikt_pickle = pickle.load(handle)


book_df,y = similar_recommendation(model_pickle, user_item_matrix_pickle,507 , user_dikt_pickle, item_dikt_pickle,threshold = 7)

z = json.dumps(y)

rec_books = json.loads(z)
