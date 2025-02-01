from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import PageForm

def index(request):
    category_list = Category.objects.order_by('-name')[:5]
    context_dict = {'boldmessage': 'Welcome to Rango! Explore the categories:',
                    'categories' : category_list
    } # to pass into the template engine

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
