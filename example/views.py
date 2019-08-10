from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
import requests
from django.core import serializers
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from pymongo import MongoClient
import pymongo
import time
import datetime


import ast

from mysite import get_recommendation, get_clicks_rating, get_review_rating, get_net_rating, myclient, mydb, mycol

from users.models import Profile

from .forms import *


client = MongoClient("mongodb://localhost:27017")


export = []
with open('exportNew.json', 'r') as myfile:
    export = json.load(myfile)

bookDetail = ''

rec_books = []
top_rated_books = []
book_search_data = []
recently_added = []


# Create your views here.
def index(request):

    global export

    global rec_books
    global top_rated_books
    global recently_added

    # global bookTitle
    # global bookAuthor
    # global genre
    # global description
    # global ISBN
    # global imageURL
    
    # Initializing the getFormData as empty strings

    bookTitle = 'bookTitle here'
    bookAuthor = ''
    genre = ''
    description = ''
    ISBN = ''
    imageURL= ''

    # db=client.test_db
    # dict={'A':[1,2,3,4,5,6]}
    # db.test_collection.insert(dict)
    # to_print=db.test_collection.find({})
    # print(to_print[0]['A'])

    # dict={'userid': request.user.id}
    # db.user_collection.insert(dict)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["majorProject"]
    mycol = mydb["bookDataset"]
    x=mycol.aggregate([{"$match":{"average_rating":{"$gt":4}}},{"$sort":{"average_rating":-1}},{"$limit":50},{"$sample":{"size":15}},{"$project":{'_id':0, 'ISBN':'$ISBN', 'genres': '$genres', 'bookTitle': '$Book-Title', 'bookAuthor': '$Book-Author', 'publicationYear': '$Year-Of-Publication', 'publisher': '$Publisher', 'imageURL': '$Image-URL', 'averageRating': '$average_rating', 'description': '$description', 'publicationYear':'$publication_year'} }])
    top_rated_books=list(x)


    # for recently added
    # limit size is changeable. Right now, it's set to 3
    y=mydb['bookDataset'].aggregate([{"$sort":{"date_added":-1}},{"$limit":10},{"$sample":{"size":15}},{"$project":{'_id':0, 'ISBN':'$ISBN', 'genres': '$genres', 'bookTitle': '$Book-Title', 'bookAuthor': '$Book-Author', 'publicationYear': '$Year-Of-Publication', 'publisher': '$Publisher', 'imageURL': '$Image-URL', 'averageRating': '$average_rating', 'description': '$description', 'publicationYear':'$publication_year'} }])
    recently_added = list(y)
    # print(recently_added)
   


    if request.user.is_authenticated:
        userId = request.user.id + 278858
        print('-------------------------------userId----------------------')
        print(userId)
        rec_books, heading = get_recommendation(userId)
        # for 'as you've last checked in' section
        lastCheckedIn = mydb['userActivity'].aggregate([{"$match":{"user_id": userId}},{"$project":{"activity":{"book_id":1,"activity":{"date_modified":1}}}},{"$unwind":"$activity"},{"$project":{"activity.book_id":1,"date_modified":"$activity.activity.date_modified"}},{"$sort":{"date_modified":-1}},{"$limit" : 1} ])
        last_check_in = list(lastCheckedIn)
        last_check_in_book_id = last_check_in[0]['activity']['book_id']
        for_last_checked_books=mycol.find({"ISBN":last_check_in_book_id})
        for_last_checked_books=list(for_last_checked_books)
        last_check_in_book = for_last_checked_books[0]['Book-Title']
        print('Last Checked In----------------------------', last_check_in_book)


    else:
        rec_books, heading = get_recommendation(0)
        print("Random Books are: ", len(rec_books))

        # Profile.objects.filter(user=request.user).update(fifteenBooks=True)

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

    
    if request.method == 'POST' and request.FILES['book_cover']:
        return HttpResponse(request.body) 
    #     form = BookCoverForm(request.POST, request.FILES) 
    #     myfile = request.FILES['book_cover']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     bookTitle = request.POST.get('Book-Title')
    #     author = request.POST.get('Book-Author')
    #     isbn = request.POST.get('ISBN')
    #     genre = request.POST.get('genre')
    #     description = request.POST.get('description') 
    #     print(bookTitle, author, isbn, genre, description)
    #     print(uploaded_file_url)
        
    #     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    #     mydb = myclient["majorProject"]
    #     date_now=datetime.datetime.now()
    #     mycol = mydb["bookDataset"]
    #     x=mydb['counter'].find({},{"book_count":1,"_id":0})
    #     new_book_id=list(x)[0]['book_count']+1
    #     a={
    #         'Book-Title': bookTitle,
    #         'Book-Author': author,
    #         'Image-URL': uploaded_file_url,
    #         'description': description,
    #         'genres': genre,
    #         'date_added':date_now
    #     }
    #     isRegister=True
    #     try:
    #         z=mycol.update({'ISBN':isbn},a)
    #         mydb['counter'].update({},{"$inc":{"book_count":1}})
    #     except:
    #         isRegister=False
    #     print(isRegister)
    #     print(new_book_id)

    #     if form.is_valid():
    #         form.save() 
    #         return redirect('index') 
    # else: 
    #     form = BookCoverForm() 
    # return render(request, 'example/index.html', {
    #     'form': form,
    #     'rec_books': rec_books,
    #     'recently_added': recently_added,
    #     'heading': heading,
    #     'top_rated': top_rated_books,
    #     'shopkeeper': shopkeeper,  
    #     'getData' : {
    #             'bookTitle': bookTitle,
    #             'bookAuthor': bookAuthor,
    #             'genre': genre,
    #             'description': description,
    #             'ISBN': ISBN,
    #             'imageURL': imageURL 
    #         }
    # }) 


    # if request.method == 'POST':
    #     # getData = request.GET.get('getData')
    #     # send some data to nodeMCU signalling that it can send the barcode data (ISBN) to the django server
    #     # do this if django server is able to get the ISBN
        
    #     # isbn_no = 0517703939 
    #     # isbn_no = str(isbn_no)

    #     isbn_no = '0886778271'

    #     url = "https://www.googleapis.com/books/v1/volumes?q=" + isbn_no
    #     response = requests.get(url)
    #     parsed = json.loads(response.text)
    #     if(parsed["totalItems"] == 0):
    #         print("Couldn't find the book")
    #     else:
    #         bookTitle = parsed["items"][0]["volumeInfo"]["title"]
    #         bookAuthor = parsed["items"][0]["volumeInfo"]["authors"]
    #         bookAuthor = ", ".join(bookAuthor)
    #         genre = parsed["items"][0]["volumeInfo"]["categories"]
    #         genre = ", ".join(genre)
    #         description = parsed["items"][0]["volumeInfo"]["description"]
    #         imageURL = parsed["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    #         print(bookTitle)
            
    #         data = {
    #             'bookTitle': bookTitle,
    #             'bookAuthor': bookAuthor,
    #             'genre': genre,
    #             'description': description,
    #             'imageURL': imageURL
    #         }
            
    #         return JsonResponse(data)

    
            
    # print(bookTitle)
    
    return render(request, 'example/index.html', 
        {
            'rec_books': rec_books, 
            'heading': heading,
            'top_rated': top_rated_books, 
            'last_check_in_book': last_check_in_book,
            'recently_added': recently_added,
            'shopkeeper': shopkeeper, 
            'getData' : {
                'bookTitle': bookTitle,
                'bookAuthor': bookAuthor,
                'genre': genre,
                'description': description,
                'ISBN': ISBN,
                'imageURL': imageURL 
            }

        })




def detail(request, isbn):

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["majorProject"]
    mycol = mydb["userActivity"]

    global export
    global bookDetail

    whichList = 0

    if whichList == 0:
        for book in rec_books:
            if book['ISBN'] == isbn:
                bookDetail = book
                whichList = 1
            else: 
                whichList = 0

    if whichList != 1:
        for book in top_rated_books:
            if book['ISBN'] == isbn:
                bookDetail = book
                whichList = 2
            else: 
                whichList = 0

    if whichList != 2:
        for book in book_search_data:
            if book['ISBN'] == isbn:
                bookDetail = book
                whichList = 3
            else:
                whichList = 0
    
    if whichList != 3:
        for book in recently_added:
            if book['ISBN'] == isbn:
                bookDetail = book
                print('-------------recently Added-----------------------')
                whichList = 4
            else:
                whichList = 0

    # if 'mainPage' in request.GET:
    #     for book in rec_books:
    #         if book['ISBN'] == isbn:
    #             bookDetail = book

    if request.user.is_authenticated:
        if request.method == 'POST':
        
            click = request.body

            if(type(click)!=bytes):
                my_click = json.loads(click.decode('utf-8'))
                get_clicked=my_click['clicked']
                get_ISBN = my_click['ISBN']
            else:
                get_clicked="notclicked"
                rating = request.POST.get('stars', " ")
                review = request.POST.get('review')


            if (get_clicked == 'clicked'):

                user_id = request.user.id + 278858
                book_id = get_ISBN

                new_clicks = 1
                new_clicks_rating=get_clicks_rating(new_clicks)
                x=mycol.find({"user_id":user_id,"activity.book_id":book_id},{"activity.$.activity":1,"_id":0})
                if x.count()==0:
                    y=mycol.find({"user_id":user_id},{"activity.$.activity":1,"_id":0})
                    if(y.count()==0):
                        mycol.insert({"user_id":user_id,"isFifteen":0,"activity":[{"book_id":book_id,"activity":{"clicks":new_clicks,"clicks_rating":new_clicks_rating,"net_rating":new_clicks_rating,"date_modified":datetime.datetime.now()}}]})
                    else:
                        mycol.update({"user_id":user_id},{"$push":{"activity":{"book_id":book_id,"activity":{"clicks":new_clicks,"clicks_rating":new_clicks_rating,"net_rating":new_clicks_rating,"date_modified":datetime.datetime.now()}}}})
                    
                else:
                    data=x[0]['activity'][0]['activity']
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
                    
                    # print("net rating is :"+str(net_rating))
                    # print("new date:"+str(datetime.datetime.now()))
                    # print("clicks rating"+str(clicks_rating))
                    mycol.update({"user_id":user_id,"activity.book_id":book_id},{"$set":{"activity.$.activity.clicks":total_clicks,"activity.$.activity.clicks_rating":clicks_rating,"activity.$.activity.net_rating":net_rating,"activity.$.activity.date_modified":datetime.datetime.now()} },upsert=True)

            if(rating == " "):
                print("---------empty--------rating")
            else:
                # print("---------------------rating given-----------------------------------")
                user_id = request.user.id + 278858
                book_id = isbn
                new_rating = rating
                
                x=mycol.find({"user_id":user_id,"activity.book_id":book_id},{"activity.$.activity":1,"_id":0})
                if x.count()==0:
                    y=mycol.find({"user_id":user_id},{"activity.$.activity":1,"_id":0})
                    if(y.count()==0):
                        mycol.insert({"user_id":user_id,"isFifteen":0,"activity":[{"book_id":book_id,"activity":{"rating":int(new_rating),"net_rating":new_rating,"date_modified":datetime.datetime.now()}}]})
                    else:
                        mycol.update({"user_id":user_id},{"$push":{"activity":{"book_id":book_id,"activity":{"rating":int(new_rating),"net_rating":new_rating,"date_modified":datetime.datetime.now()}}}})
                    
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
                    # print("clicks_rating is:"+str(clicks_rating))
                    # print("review rating is:"+str(review_rating))
                    # print("new rating is:"+str(new_rating))
                    # print("net"+str(net_rating))
                    # print("new date:"+str(datetime.datetime.now()))
                    mycol.update({"user_id":user_id,"activity.book_id":book_id},{"$set":{"activity.$.activity.rating":int(new_rating),"activity.$.activity.net_rating":net_rating,"activity.$.activity.date_modified":datetime.datetime.now()} },upsert=True)

            if(review == " "):
                print("---------empty--------review")
            else:
                # print("--------------------------------review given----------------------------")
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
                    # print("review rating:"+str(review_rating))
                    # print("rating:"+str(rating))
                    # print("clicks rating:"+str(clicks_rating))
                    # print("net rating is :"+str(net_rating))
                    # print("new date:"+str(datetime.datetime.now()))
                    # print("net"+str(rating))
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

    hey = "yo"
    
    return render(request, 'example/detail.html', {'b': bookDetail, 'e': rec_books, 'hey': hey, 'shopkeeper': shopkeeper})



# def index(request):
#     with open('export.json', 'r') as myfile:
#         export = json.load(myfile)
#         print(type(j))
#         return render(request, 'example/index.html', )
    
    
def getData(request):
    print('this is the ice cool summer')
    isbn_no=""
    try:
        myclient = MongoClient("mongodb://localhost:27017")
        mydbs=myclient['majorProject']
        barcode_col=mydbs['tempBarcode']
        book_col=mydbs['bookDataset']
        x=barcode_col.find({"userId":"3000"}).sort('dateAdded',-1).limit(1)
        barcode_data=list(x)
        # isbn_no = str(1250178959)
        isbn_no=barcode_data[0]['ISBN']
        print('the isbn no is',isbn_no)
        y=book_col.find({"isbn13":int(isbn_no)})
        dataset_book=list(y)
        if(len(dataset_book)>0):
            bookTitle =dataset_book[0]['Book-Title'] 
            bookAuthor =dataset_book[0]['Book-Author'] 
            genre ="Children" 
            # genre =dataset_book[0]['genres'] 
            description =dataset_book[0]['description'] 
            imageURL =dataset_book[0]['Image-URL'] 
            request_message ="book already exists on the server database"    
        else:
            url = "https://www.googleapis.com/books/v1/volumes?q=" + isbn_no
            response = requests.get(url)
            parsed = json.loads(response.text)
            print("the length is",len(parsed))
            if(parsed["totalItems"] == 0):
                print("Couldn't find the book")
                raise Exception('error')
            else:
                bookTitle = parsed["items"][0]["volumeInfo"]["title"]
                bookAuthor = parsed["items"][0]["volumeInfo"]["authors"]
                bookAuthor = ", ".join(bookAuthor)
                genre = parsed["items"][0]["volumeInfo"]["categories"]
                genre = ", ".join(genre)
                description = parsed["items"][0]["volumeInfo"]["description"]
                imageURL = parsed["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
                request_message="book details fetched from google books api"
    except Exception as e:
        print("the exception is ",e)
        if request.method == 'POST':
            print("the case of mismatched")
            bookTitle= "",
            bookAuthor= "",
            genre= "",
            description= "",
            imageURL= "",
            request_message="book details could not be fetched"            
    data = {
                'bookTitle': bookTitle,
                'bookAuthor': bookAuthor,
                'genre': genre,
                'description': description,
                'imageURL': imageURL,
                'ISBN':isbn_no,
                'request_message':request_message
            }
    return JsonResponse(data)
    # return redirect('index')


def add_book(request):
    # a=request.POST
    print('hello world')
    # return HttpResponse(request.POST)
    form = BookCoverForm(request.POST, request.FILES) 
    myfile = request.FILES['book_cover']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    bookTitle = request.POST.get('Book-Title')
    author = request.POST.get('Book-Author')
    isbn = request.POST.get('ISBN')
    genre = request.POST.get('genre')
    description = request.POST.get('description') 
    print(bookTitle, author, isbn, genre, description)
    print(uploaded_file_url)
    
    # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # mydb = myclient["majorProject"]
    # date_now=datetime.datetime.now()
    # mycol = mydb["bookDataset"]
    # x=mydb['counter'].find({},{"book_count":1,"_id":0})
    # new_book_id=list(x)[0]['book_count']+1
    a={
        'Book-Title': bookTitle,
        'Book-Author': author,
        'Image-URL': uploaded_file_url,
        'description': description,
        'genres': genre,
        'date_added':date_now
    }
    isRegister=True
    try:
        z=mycol.update({'ISBN':isbn},a)
        mydb['counter'].update({},{"$inc":{"book_count":1}})
    except:
        isRegister=False
    print(isRegister)
    print(new_book_id)

    if form.is_valid():
        form.save() 
        return redirect('index') 
    else: 
        form = BookCoverForm() 
    return render(request, 'example/index.html', {
        'form': form,
        'rec_books': rec_books,
        'recently_added': recently_added,
        'heading': heading,
        'top_rated': top_rated_books,
        'shopkeeper': shopkeeper,  
        'getData' : {
                'bookTitle': bookTitle,
                'bookAuthor': bookAuthor,
                'genre': genre,
                'description': description,
                'ISBN': ISBN,
                'imageURL': imageURL 
            }
    }) 

def search(request):

    global book_search_data

    if 'search' in request.GET:
        print('------------------------searched--------------------------------')
        searchString = request.GET.get('search')

        book_search_variable= searchString
        w=mydb['bookDataset'].aggregate([{"$match":{"Book-Title":{"$regex":book_search_variable}}},
                    {"$project":{'_id':0,'ISBN':'$ISBN', 'bookTitle':'$Book-Title','bookAuthor':'$Book-Author','genres':'$genres','imageURL':'$Image-URL','averageRating':'$average_rating','publicationYear':'$publication_year','description':'$description'} },{"$limit":15}])
        book_search_data = list(w) 
        print(book_search_data)       

    return render(request, 'example/search.html', {'searchResult': book_search_data})

@csrf_exempt
def barcode(request):
    if request.method == 'POST':
        # print(request.body)
        # print(request.body)
        data=json.loads(request.body.decode('utf-8'))
        print("data is ",data)
        print("type is",type(data))
        try:
            apiKey=data['apiKey']
            if(apiKey!="9GbIKGunRvsEgzOOXAqYXfySvfnEX2WE"):
                raise Exception('keyerror')
            userId=data['userId']
            ISBN=data['ISBN']
            mydb = client["majorProject"]
            mycol = mydb["tempBarcode"]
            mycol.insert({"dateAdded":datetime.datetime.now(),"userId":userId,"ISBN":ISBN})

            response={"status":"okay","message":{'ISBN':ISBN,"state":"okay"}}
        except:
            print('hello')
            response={"status":"error","message":"couldnot parse data input properly"}
        # data=json.loads(str(request.body))
        # print("the request body is",request.body.userId,request.body.apiKey,request.body.ISBN)
        # response={"status":"oay","message":"all is well"}
        return JsonResponse(response)
    else:
        return HttpResponse('you have no authority to access this site')