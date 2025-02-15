import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    python_cat = add_cat('Python')
    add_page(cat = python_cat, title = "Official Python Tutorial", 
             url = "https://docs.python.org/3/tutorial/")
    add_page(cat = python_cat, title = "Learn Python in 10 Minutes",
             url = "https://wwww.korokithakis.net/tutorials/python/")
    django_cat = add_cat('Django')
    add_page(cat = django_cat, title = "Official Django Tutorial", 
             url = "https://docs.djangoproject.com/en/2.1/intro/tutorial01/")
    for cat in Category.objects.all():
        print(f"- {cat.name}")
def add_page(cat, title, url, views = 0):
    p = Page.objects.get_or_create(category = cat, title = title) [0]
    p.url = url
    p.views = views
    p.save()
    return p
def add_cat(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    return c
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
    

                      