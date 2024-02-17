from django.urls import path
from . import views

app_name = 'testapp'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('features/', views.features_view, name='features'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]
