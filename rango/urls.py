from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name = 'index'), # maps the empty string to the index view
    path('about/', views.about, name='about'),
    path('', views.index, name = 'index'),
    path('category/<str:category_name>/', views.show_category, name = 'show_category'),
    path('category/<str:category_name>/add_page/', views.add_page, name='add_page'),
]