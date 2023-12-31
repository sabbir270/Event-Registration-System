from django.urls import path
from . import views
app_name = 'eventapp'
urlpatterns = [
    path('',views.home,name='home'),
    path('userRegistration/',views.register_user,name='userRegistration'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    
]