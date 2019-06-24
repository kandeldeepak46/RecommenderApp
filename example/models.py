from django.db import models
from PIL import Image

# Create your models here.
class BookCover(models.Model): 
    book_cover = models.ImageField(upload_to='media/') 