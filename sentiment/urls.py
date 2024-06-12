from django.urls import path
from .views import sentiment_view

urlpatterns = [
     
    path('', sentiment_view, name='sentiment_view'),
]