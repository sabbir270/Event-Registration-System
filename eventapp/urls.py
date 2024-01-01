from django.urls import path
from . import views
app_name = 'eventapp'
urlpatterns = [
    path('',views.home,name='home'),
    path('userRegistration/',views.register_user,name='userRegistration'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    path('enroll/<int:event_id>/', views.enroll_for_event, name='enroll-event'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
     path('events/<int:event_id>/unregister/', views.unregister_from_event, name='unregister-from-event'),
    
]