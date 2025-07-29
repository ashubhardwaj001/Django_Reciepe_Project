from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,Sum
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



def get_students(request):

    queryset = Student.objects.all()

    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = Student.objects.filter(Q(student_name__icontains=search) | Q(department__department__icontains=search)
                                          | Q(student_id__student_id__icontains=search) | Q(student_email__icontains=search))


        
    paginator = Paginator(queryset, 10) 
    page_number = request.GET.get('page', 1)

    page_obj = paginator.get_page(page_number)

    return render(request, 'report/students.html', {'queryset': page_obj})


from .seed import generate_report_card
def see_marks(request, student_id):

    # generate_report_card()

    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))

    current_rank = ReportCard.objects.filter(student__student_id__student_id=student_id).first().student_rank
    date_of_result = ReportCard.objects.filter(student__student_id__student_id=student_id).first().date_of_report_card_generation



    return render(request, 'report/marks.html', {'queryset': queryset, 'total_marks': total_marks, 'current_rank': current_rank, 'date_of_result': date_of_result})





