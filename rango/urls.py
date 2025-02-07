from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name = 'index'), # maps the empty string to the index view
    path('about/', views.about, name='about'),
    path('category/<str:category_name>/', views.show_category, name = 'show_category'),
    path('category/<str:category_name>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]