from django.shortcuts import render

# Create your views here.
from .sentiment_model import predict_sentiment

def sentiment_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            sentiment = predict_sentiment(text)
            sentiment_map = {0: 'negative', 1: 'positive', 2: 'neutral'}
            return render(request, 'sentiment/result.html', {'sentiment': sentiment_map[sentiment], 'text': text})
    return render(request, 'sentiment/form.html')
