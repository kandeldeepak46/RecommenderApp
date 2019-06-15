from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from django.template.loader import render_to_string

from django.core.files.storage import FileSystemStorage

from pymongo import MongoClient
import pymongo
import time
import datetime

import ast

from mysite import rec_books, get_clicks_rating, get_review_rating, get_net_rating

from users.models import Profile


client = MongoClient("mongodb://110.34.31.28:27017")

export = []
with open('exportNew.json', 'r') as myfile:
    export = json.load(myfile)

bookDetail = ''


# Create your views here.
def index(request):

    global export

    # db=client.test_db
    # dict={'A':[1,2,3,4,5,6]}
    # db.test_collection.insert(dict)
    # to_print=db.test_collection.find({})
    # print(to_print[0]['A'])

    # dict={'userid': request.user.id}
    # db.user_collection.insert(dict)

    if request.method == 'POST':
        bookImg = request.POST.get('Image-URL-L')
        bookTitle = request.POST.get('Book-Title')
        author = request.POST.get('Book-Author')
        isbn = request.POST.get('ISBN')
        genre = request.POST.get('genre')
        description = request.POST.get('description')

        # db=client.test_db
        # dict={
        #     'bookImg': bookImg,
        #     'bookTitle': bookTitle,
        #     'author': author,
        #     'isbn': isbn,
        #     'genre': genre,
        #     'description': description
        #     }
        # db.test_collection.insert(dict)

    if request.user.is_authenticated:
        userId = request.user.id + 278858
        Profile.objects.filter(user=request.user).update(fifteenBooks=True)
        

        print ("-----------------------------Profile Update------------------------------")

        # db=client.test_db
        # dict={
        #     'userId': userId
        #     }
        # db.new_user.insert(dict)



    if request.user.is_authenticated:
        if (request.user.profile.role == 'Shopkeeper'):
            shopkeeper = 'yes'
        else: 
            shopkeeper = 'no'
    else: 
        shopkeeper = 'no'

    
    return render(request, 'example/index.html', {'rec_books': rec_books, 'shopkeeper': shopkeeper})


def detail(request, isbn):

    myclient = pymongo.MongoClient("mongodb://110.34.31.28:27017/")
    mydb = myclient["majorProject"]
    mycol = mydb["userActivity"]

    global export
    global bookDetail

    for book in rec_books:
        if book['ISBN'] == isbn:
            bookDetail = book

    if request.user.is_authenticated:
        if request.method == 'POST':
            rating = request.POST.get('stars', " ")
            review = request.POST.get('review', " ")

            click = ast.literal_eval(request.body.decode("utf-8"))
            # print('________________________________________________________________________')
            # print(click)
            # print('________________________________________________________________________')

            # bookClick = click.get(clicked, 0)
        
            if (click['clicked'] == 'clicked'):
                user_id = request.user.id + 278858
                book_id = isbn
                new_clicks = 1
                new_clicks_rating=get_clicks_rating(new_clicks)
                x=mycol.find({"user_id":user_id,"activity.book_id":book_id},{"activity.$.activity":1,"_id":0})
                if x.count()==0:
                    y=mycol.find({"user_id":user_id},{"activity.$.activity":1,"_id":0})
                    if(y.count()==0):
                        mycol.insert({"user_id":user_id,"is_fifteen":0,"activity":[{"book_id":book_id,"activity":{"clicks":new_clicks,"clicks_rating":new_clicks_rating,"net_rating":new_clicks_rating,"date_modified":datetime.datetime.now()}}]})
                    else:
                        mycol.update({"user_id":user_id},{"$push":{"activity":{"book_id":book_id,"activity":{"clicks":new_clicks,"clicks_rating":new_clicks_rating,"net_rating":new_clicks_rating,"date_modified":datetime.datetime.now()}}}})
                    
                else:
                    data=x[0]['activity'][0]['activity']
                    print(data)
                    try:
                        rating=float(data['rating'])
                    except:
                        rating=0
                    try:
                        review_rating=float(data['review_rating'])
                    except:
                        review_rating=0
                    try:
                        clicks=int(data['clicks'])
                    except:
                        clicks=0
                    total_clicks=new_clicks+clicks
                    clicks_rating=get_clicks_rating(total_clicks)
                    net_rating=get_net_rating(review_rating,rating,clicks_rating)
                    
                    print("net rating is :"+str(net_rating))
                    print("new date:"+str(datetime.datetime.now()))
                    print("clicks rating"+str(clicks_rating))
                    mycol.update({"user_id":user_id,"activity.book_id":book_id},{"$set":{"activity.$.activity.clicks":total_clicks,"activity.$.activity.clicks_rating":clicks_rating,"activity.$.activity.net_rating":net_rating,"activity.$.activity.date_modified":datetime.datetime.now()} },upsert=True)

            if(rating == " "):
                print("---------empty--------rating")
            else:
                user_id = request.user.id + 278858
                book_id = isbn
                new_rating = rating
                x=mycol.find({"user_id":user_id,"activity.book_id":book_id},{"activity.$.activity":1,"_id":0})
                if x.count()==0:
                    y=mycol.find({"user_id":user_id},{"activity.$.activity":1,"_id":0})
                    if(y.count()==0):
                        mycol.insert({"user_id":user_id,"isFifteen":0,"activity":[{"book_id":book_id,"activity":{"rating":new_rating,"net_rating":new_rating,"date_modified":datetime.datetime.now()}}]})
                    else:
                        mycol.update({"user_id":user_id},{"$push":{"activity":{"book_id":book_id,"activity":{"rating":new_rating,"net_rating":new_rating,"date_modified":datetime.datetime.now()}}}})
                    
                else:
                    data=x[0]['activity'][0]['activity']
                    print(data)
                    try:
                        clicks_rating=float(data['clicks_rating'])
                    except:
                        clicks_rating=0
                    try:
                        review_rating=float(data['review_rating'])
                    except:
                        review_rating=0
                    net_rating=get_net_rating(review_rating,new_rating,clicks_rating)
                    print("clicks_rating is:"+str(clicks_rating))
                    print("review rating is:"+str(review_rating))
                    print("new rating is:"+str(new_rating))
                    print("net"+str(net_rating))
                    print("new date:"+str(datetime.datetime.now()))
                    mycol.update({"user_id":user_id,"activity.book_id":book_id},{"$set":{"activity.$.activity.rating":new_rating,"activity.$.activity.net_rating":net_rating,"activity.$.activity.date_modified":datetime.datetime.now()} },upsert=True)

            if(review == " "):
                print("---------empty--------rating")
            else:
                user_id= request.user.id + 278858
                book_id= isbn
                new_review = review
                new_review_rating=get_review_rating(new_review)

                x=mycol.find({"user_id":user_id,"activity.book_id":book_id},{"activity.$.activity":1,"_id":0})
                if x.count()==0:
                    y=mycol.find({"user_id":user_id},{"activity.$.activity":1,"_id":0})
                    if(y.count()==0):
                        mycol.insert({"user_id":user_id,"isFifteen":0,"activity":[{"book_id":book_id,"activity":{"review":new_review,"review_rating":new_review_rating,"net_rating":new_review_rating,"date_modified":datetime.datetime.now()}}]})
                    else:
                        mycol.update({"user_id":user_id},{"$push":{"activity":{"book_id":book_id,"activity":{"review":new_review,"review_rating":new_review_rating,"net_rating":new_review_rating,"date_modified":datetime.datetime.now()}}}})
                    
                else:
                    data=x[0]['activity'][0]['activity']
                    print(data)
                    try:
                        rating=float(data['rating'])
                    except:
                        rating=0
                    try:
                        clicks_rating=float(data['clicks_rating'])
                    except:
                        clicks_rating=0
                    
                    review_rating=get_review_rating(new_review)
                    net_rating=get_net_rating(review_rating,rating,clicks_rating)    
                    print("review rating:"+str(review_rating))
                    print("rating:"+str(rating))
                    print("clicks rating:"+str(clicks_rating))
                    print("net rating is :"+str(net_rating))
                    print("new date:"+str(datetime.datetime.now()))
                    print("net"+str(rating))
                    mycol.update({"user_id":user_id,"activity.book_id":book_id},{"$set":{"activity.$.activity.review":new_review,"activity.$.activity.review_rating":review_rating,"activity.$.activity.net_rating":net_rating,"activity.$.activity.date_modified":datetime.datetime.now()} },upsert=True)

            # readIt = ast.literal_eval(request.body.decode("utf-8"))

            # if (readIt == None):
            #     print("Yo buddy");    
            # clicked = False
            # if (click['clicked'] == 'clicked'):
            #     clicked = True
            # readIt = readIt['readIt']
            # print(readIt)
    
            # print(request.body.decode("utf-8")) 
            # data = json.loads(request.body.decode("utf-8"))
            # s = json.dumps(data, indent=4, sort_keys=True)
            # print(type(s))
            # userId = request.user.id + 278858

            # db=client.test_db
            # dict={
            #     'userId': userId,
            #     'isbn': isbn,
            #     'rating': rating,
            #     'review': review,
            #     'clicked': clicked,
            #     'readIt': readIt
            #     }
            # db.rating_collection.insert(dict)
        

    if request.user.is_authenticated:
        if (request.user.profile.role == 'Shopkeeper'):
            shopkeeper = 'yes'
        else: 
            shopkeeper = 'no'
    else: 
        shopkeeper = 'no'

    
    
    return render(request, 'example/detail.html', {'b': bookDetail, 'e': rec_books, 'shopkeeper': shopkeeper})



# def index(request):
#     with open('export.json', 'r') as myfile:
#         export = json.load(myfile)
#         print(type(j))
#         return render(request, 'example/index.html', )
    
    

    



    