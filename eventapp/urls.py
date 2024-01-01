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
    
    #Api_url
    path('api/events/', views.EventList.as_view(), name='event-list'),
    path('api/event-details/<int:pk>/', views.EventDetail.as_view(), name='event-detail'),  
    path('api/user-registered-events/', views.user_registered_events, name='user-registered-events'),
    path('api/enroll-for-event/<int:event_id>/', views.enroll_event, name='enroll-for-event'),
] 
