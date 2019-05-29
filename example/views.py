from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from django.template.loader import render_to_string

export = []
with open('exportNew.json', 'r') as myfile:
    export = json.load(myfile)



# Create your views here.
def index(request):
    global export
    return render(request, 'example/index.html', {'e': export})

def detail(request, isbn):
    global export

    for book in export:
        if book['ISBN'] == isbn:
            bookDetail = book
    
    return render(request, 'example/detail.html', {'b': bookDetail, 'e': export})



# def index(request):
#     with open('export.json', 'r') as myfile:
#         export = json.load(myfile)
#         print(type(j))
#         return render(request, 'example/index.html', )
    
    

    



    