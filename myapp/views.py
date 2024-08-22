from django.shortcuts import render

# Create your views here.
def home(request):
    context = {"message": "Hello, World!"}
    return render(request, 'home.html', context)