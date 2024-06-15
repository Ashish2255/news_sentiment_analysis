# from django.urls import path
# from .views import sentiment_view

# urlpatterns = [
     
#     path('', sentiment_view, name='sentiment_view'),
# ]
# urls.py
from django.urls import path
from .views import sentiment_view, LoginPage, SignupPage, LogoutPage, user_history, delete_history,view_history

urlpatterns = [
    path('sentiment/', sentiment_view, name='sentiment_view'),
    path('login/', LoginPage, name='login'),
    path('signup/', SignupPage, name='signup'),
    path('logout/', LogoutPage, name='logout'),
    # path('history/', user_history, name='user_history'),
    path('delete/<int:history_id>/', delete_history, name='delete_history'),
    path('view/<int:history_id>/', view_history, name='view_history'),
]
