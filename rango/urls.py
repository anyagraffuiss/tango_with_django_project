from django.urls import path
from rango import views

app_name = 'rango'
urlpatterns = [
    path('', views.index, name = 'index'), # Home page
    path('about/', views.about, name='about'), # About page
    path('category/<str:category_name>/', views.show_category, name = 'show_category'), # View category
    path('category/<str:category_name>/add_page/', views.add_page, name='add_page'), # Add a page to the category
    path('register/', views.register, name='register'), # Register a new user
    path('login/', views.user_login, name='login'), # Login page
    path('logout/', views.user_logout, name='logout'), # Logout page
    path('restricted/', views.restricted, name='restricted'), # Restricted page
    path('test_cookie/', views.test_cookie, name='test_cookie'), # Test cookie functionality
]