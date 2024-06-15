from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import SearchHistory
from .sentiment_model import predict_sentiment

@login_required(login_url='login')
def sentiment_view(request):
    user_history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            sentiment = predict_sentiment(text)
            sentiment_map = {0: 'negative', 1: 'positive', 2: 'neutral'}
            # Save the search history
            SearchHistory.objects.create(user=request.user, text=text, sentiment=sentiment_map[sentiment])
            return render(request, 'sentiment/result.html', {'sentiment': sentiment_map[sentiment], 'text': text, 'user_history': user_history})
    return render(request, 'sentiment/form.html', {'user_history': user_history})

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('sentiment_view')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, 'sentiment/login.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'sentiment/signup.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def user_history(request):
    user_history = SearchHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'sentiment/user_history.html', {'user_history': user_history})

@login_required(login_url='login')
def delete_history(request, history_id):
    history_item = SearchHistory.objects.get(id=history_id, user=request.user)
    history_item.delete()
    return redirect('sentiment_view')

@login_required(login_url='login')
def view_history(request, history_id):
    history_item = get_object_or_404(SearchHistory, id=history_id, user=request.user)
    return render(request, 'sentiment/details.html', {'history': history_item})