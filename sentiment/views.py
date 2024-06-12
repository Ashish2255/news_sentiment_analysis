
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from .sentiment_model import predict_sentiment
@login_required(login_url='login')
def sentiment_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            sentiment = predict_sentiment(text)
            sentiment_map = {0: 'negative', 1: 'positive', 2: 'neutral'}
            return render(request, 'sentiment/result.html', {'sentiment': sentiment_map[sentiment], 'text': text})
    return render(request, 'sentiment/form.html')
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('sentiment_view')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'sentiment/login.html')
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        



    return render (request,'sentiment/signup.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')