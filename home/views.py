from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    peoples = [
        {'name': 'John', 'age': 30},
        {'name': 'Jane', 'age': 25},
        {'name': 'Doe', 'age': 22},
        {'name': 'Alice', 'age': 28},
        {'name': 'Bob', 'age': 35}
    ]

    vegetables = ['Carrot', 'Broccoli', 'Spinach', 'Potato', 'Tomato']
    return render(request, 'index.html', context={'peoples': peoples, 'vegetables': vegetables, 'page': 'home'})


def about(request):
    context = {'page': 'about'}
    return render(request, 'about.html', context)

def contact(request):
    context = {'page' : 'contact'}
    return render(request, 'contact.html',context)

def success_page(request):
    return HttpResponse("<h1>This is the Success Page!</h1>")
