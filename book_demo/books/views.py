from django.shortcuts import render
from rest_framework import viewsets

from .models import Books
from .serializer import BookSerializer

# Create your views here.

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer