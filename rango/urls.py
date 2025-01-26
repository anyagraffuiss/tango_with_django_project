from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name = 'index'), # maps the empty string to the index view
    path('about/', views.about, name='about'),
]