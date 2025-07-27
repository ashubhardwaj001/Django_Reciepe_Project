from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def receipes(request):
    # This view will render the recipes page
    if request.method == 'POST':
        # Handle form submission or other POST logic here
        data = request.POST  

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')  

        # Save the recipe to the database

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        
        return redirect('/receipes/')  
    
    
    
    queryset = Receipe.objects.all() 

    if request.GET.get('search'):

        queryset = Receipe.objects.filter(
            receipe_name__icontains=request.GET.get('search')
        )

    context = {
        'receipes': queryset
    }
    return render(request, 'receipes.html', context)


def delete_receipe(request, id):
    # This view will delete a recipe
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')

def update_receipe(request, id):

    queryset = Receipe.objects.get(id=id)
    context = {
        'receipe': queryset
    }

    if request.method == 'POST':
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        # Update the recipe in the database
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.save()

        return redirect('/receipes/')

    return render(request, 'update-receipes.html', context)


def login_page(request):

    return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username already exists')
            return render(request, 'register.html')
            

        # Create a new user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password) 
        user.save()  

        messages.info(request, 'Account created successfully')

        return redirect('/register/')

    return render(request, 'register.html')
