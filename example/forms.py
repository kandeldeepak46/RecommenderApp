from django import forms 
from .models import *
  
class BookCoverForm(forms.ModelForm): 
  
    class Meta: 
        model = BookCover
        fields = ['book_cover'] 