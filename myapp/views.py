from django.shortcuts import render, HttpResponse

def index(request):
    return HttpResponse('Welcome!')

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    return HttpResponse('Read :' + id)
