from django.shortcuts import render


def index(request, show='default'):
    return render(request, 'index2.html')


def menuSelect(request):
    return render(request, 'index.html')


