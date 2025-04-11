from django.urls import path
app_name = 'user'
from users import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('user_cart/', views.user_cart, name='user_cart'),
]