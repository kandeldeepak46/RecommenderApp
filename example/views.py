from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from django.template.loader import render_to_string

from django.core.files.storage import FileSystemStorage

from pymongo import MongoClient

import ast

from mysite import rec_books

client = MongoClient("mongodb://110.34.31.28:27017")

export = []
with open('exportNew.json', 'r') as myfile:
    export = json.load(myfile)

bookDetail = ''


# Create your views here.
def index(request):

    print(rec_books[0])

    global export

    # db=client.test_db
    # dict={'A':[1,2,3,4,5,6]}
    # db.test_collection.insert(dict)
    # to_print=db.test_collection.find({})
    # print(to_print[0]['A'])

    # dict={'userid': request.user.id}
    # db.user_collection.insert(dict)

    print(request.user.id)

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

        print (userId)

        db=client.test_db
        dict={
            'userId': userId
            }
        db.new_user.insert(dict)



    if request.user.is_authenticated:
        if (request.user.profile.role == 'Shopkeeper'):
            shopkeeper = 'yes'
        else: 
            shopkeeper = 'no'
    else: 
        shopkeeper = 'no'

    
    return render(request, 'example/index.html', {'rec_books': rec_books, 'shopkeeper': shopkeeper})


def detail(request, isbn):

    global export
    global bookDetail

    for book in rec_books:
        if book['ISBN'] == isbn:
            bookDetail = book

    if request.user.is_authenticated:
        if request.method == 'POST':
            rating = request.POST.get('stars')
            review = request.POST.get('review')

            click = ast.literal_eval(request.body.decode("utf-8"))
            readIt = ast.literal_eval(request.body.decode("utf-8"))
            if (readIt == None):
                print("Yo buddy");    
            clicked = False
            if (click['clicked'] == 'clicked'):
                clicked = True
            readIt = readIt['readIt']
            print(readIt)

            
                
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
    
    

    



    