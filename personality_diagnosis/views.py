from django.shortcuts import render

def index(request):
    return render(request, 'personality_diagnosis/index.html')
