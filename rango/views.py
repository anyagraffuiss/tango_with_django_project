from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
import datetime

def index(request):
    # get the top categories
    category_list = Category.objects.order_by('-name')[:5]

    # get the visit count from the last session
    visits = request.session.get('visits', 1)

    # get the last visit time from the session
    last_visit_str = request.session.get('last_visit', str(datetime.datetime.now()))

    # convert last visit time from string to datetime
    try:
        last_visit_time = datetime.datetime.strptime(last_visit_str[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        last_visit_time = datetime.datetime.now()

    # check if the visit is from a different day, if true: increment visit count
    if (datetime.datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.datetime.now())

    # update session data
    request.session['visits'] = visits


    context_dict = {
        'boldmessage': 'Welcome to Rango! Explore the categories',
        'categories': category_list,
        'visits': visits,
    }

    return render(request, 'rango/index.html', context = context_dict) # render response & return it 

def about(request):
    # retrieve visit count from session
    visits = request.session.get('visits', 0)
    context_dict = {
        'boldmessage' : 'This is the About Page for Rango!',
        'visits' : visits,
        }
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name):
    context_dict = {}

    try: # retrieve the category with a specified name
        category = Category.objects.get(name = category_name)
        pages = Page.objects.filter(category = category)
        context_dict['category'] = category
        context_dict['pages'] = pages

    except Category.DoesNotExist: # if the category does not exist: pass in None
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context = context_dict)

@login_required
def add_page(request, category_name):
    try: # retrieve the category to which a new page will be added 
        category = Category.objects.get(name = category_name)

    except Category.DoesNotExist:
        category = None

    if category is None: # redirect to index if the category doesnt exist 
        return redirect('rango:index')
    
    form = PageForm() # initialise a new form for adding a page

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit = False)
            page.category = category
            page.save()
            return redirect('rango:show_category', category_name = category.name)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category':category, 'category_name':category_name}   
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            # save the user object and set password
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # create and link user profile
            profile = profile_form.save(commit=False)
            profile.user = user

            # save the profile picture if provided

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })
    
def user_login(request):
    # get username and password from the form
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('rango:index') # redirect to homepage
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponse("Invalid login details. Please try again.")
    return render(request, 'rango/login.html') # render login page

@login_required
def user_logout(request):
    # logout the user and redirect to the index page
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))
@login_required
def restricted(request):
    # restricted view only for logged-in users]
    return render(request, 'rango/restricted.html')

def test_cookie(request):
    # test the functionality of cookies
    if not request.session.test_cookie_worked():
        request.session.set_test_cookie()
        return HttpResponse("Test cookie set. Reload the page to test.")
    else:
        request.session.delete_test_cookie()
        return HttpResponse("Cookie test passed.")

 