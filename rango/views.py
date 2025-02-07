from django.shortcuts import render, redirect
from rango.models import Category, Page
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 


def index(request):
    category_list = Category.objects.order_by('-name')[:5]
    context_dict = {'boldmessage': 'Welcome to Rango! Explore the categories:',
                    'categories' : category_list
    } # to pass into the template engine

    # get the number of visits from the session
    visits = request.session.get('visits', 1)
    request.session['visits'] = visits + 1

    context_dict['visits'] = visits

    return render(request, 'rango/index.html', context = context_dict) # render response & return it 

def about(request):
    context_dict = {
        'boldmessage' : 'This is the About Page for Rango!'}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name):
    context_dict = {}

    try:
        category = Category.objects.get(name = category_name)
        pages = Page.objects.filter(category = category)
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context = context_dict)

def add_page(request, category_name):
    try:
        category = Category.objects.get(name = category_name)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('rango:index')
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(comit = False)
            page.category = category
            page.save()
            return redirect('rango:show_category', category_name = category.name)
    context_dict = {'form': form, 'category':category, 'category_name':category_name}   
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

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


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))
    

