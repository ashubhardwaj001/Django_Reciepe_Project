from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def delete_receipe(request, id):
    # This view will delete a recipe
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('/receipes/')

@login_required(login_url='/login/')
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

    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Username does not exist')
            return redirect('/login/')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, 'Invalid password')
            return redirect('/login/')
        else:
            # Log the user in
            login(request, user)
            return redirect('/receipes/')


    return render(request, 'login.html')

@login_required(login_url='/login/')
def logout_page(request):
    # This view will log out the user
    logout(request)
    return redirect('/login/')

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
