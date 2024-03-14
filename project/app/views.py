from django.shortcuts import render,redirect
from .models import Book,IssuedItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

from datetime import date
from django.core.paginator import Paginator
# Create your views here.
def base(request):
    return render(request,'base.html')

def user_login(request):
    if request.method=='POST':
         username=request.POST.get('username')
         password1=request.POST.get('pass')
         user=authenticate(request,username=username,password=password1)
         if user is not None:
             login(request,user)
             return redirect(base)
         else:
             messages.info(request,'user not exists')
             print ('user not exists')
             return redirect(user_login)
         
    return render(request,'login.html')

def user_signup(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password1=request.POST.get('pass')
        password2=request.POST.get('cpass')
        if password1==password2:
            if User.objects.filter(username=username,email=email).exists():
                messages.info(request,'username already exists!!!!')
                print ("already have")
            else:
                new_user=User.objects.create_user(username,email,password1)
                new_user.save()
                return redirect(user_login)
        else:
            print('wrong password')        
    return render(request,'signup.html')

def user_logout(request):
    logout(request)
    return redirect(user_login)

@login_required(login_url='loginn')
def issue(request):
    if(request.method=='POST'):
        book_id = request.POST['book_id']
        current_book = Book.objects.get(id=book_id)
        book = Book.objects.filter(id=book_id)
        issue_item = IssuedItem.objects.create(user_id=request.user,book_id=current_book)
        issue_item.save()
        book.update(quantity = book[0].quantity-1) 

        messages.success(request,'Book isued successfully.')
    


    my_items = IssuedItem.objects.filter(user_id=request.user,return_date__isnull=True).values_list('book_id')
    books = Book.objects.exclude(id__in=my_items).filter(quantity__gt=0)

    return render(request,'issued_item.html',{'books':books})

# History view to show history of issued books to user
@login_required(login_url='login')
def history(request):

    # Get all issued books to user
    my_items = IssuedItem.objects.filter(user_id=request.user).order_by('-issue_date')

    # Paginate data
    paginator = Paginator(my_items,10) 

    # Get page number from request
    page_number = request.GET.get('page')
    show_data_final = paginator.get_page(page_number)

    # Return history page with issued books to user
    return render(request,'history.html',{'books':show_data_final})


# Return view to return book to library
@login_required(login_url='login')
def return_item(request):

    # If request is post then get book id from request
    if(request.method == 'POST'):

        # Get book id from request
        book_id = request.POST['book_id']

        # Get book object
        current_book = Book.objects.get(id=book_id)

        # Update book quantity
        book = Book.objects.filter(id=book_id)
        book.update(quantity = book[0].quantity+1)

        # Update return date of book and show success message
        issue_item = IssuedItem.objects.filter(user_id=request.user,book_id=current_book,return_date__isnull=True)
        issue_item.update(return_date=datetime.now)
        messages.success(request, 'Book returned successfully.')

    # Get all books which are issued to user
    my_items = IssuedItem.objects.filter(user_id = request.user,return_date__isnull=True).values_list('book_id')
    
    # Get all books which are not issued to user
    books = Book.objects.exclude(~Q(id__in=my_items))

    # Return return page with books that are issued to user
    params = {'books':books}
    return render(request,'return_item.html',params)
