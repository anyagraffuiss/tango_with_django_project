from django.shortcuts import render

def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'} # to pass into the template engine
    return render(request, 'rango/index.html', context = context_dict) # render response & return it 

def about(request):
    return render(request, 'rango/about.html')