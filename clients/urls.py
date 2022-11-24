from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

urlpatterns = [
    # user profile control
    path('login/', AdminLoginView.as_view(), name='login'),
    path('logout/', user_exit, name='logout'),
    path('registration/', CreateUser.as_view(), name='register'),

    # functionalities
    path('', main_page_clients, name='home'),                   # main menu
    path('make_appointment/', make_appointment, name='make_appointment'),   # view doctors and filter
    path('my_appointments/', my_appointments, name='my_appointments'),      # appointments of current user

    # ajax
    path('filter-data/', filter_data, name='filter_data'),
    path('delete_appointment/', login_required(delete_appointment), name='delete_appointment'),

    path('create_appointment/<slug:doctor_id>', login_required(ShowDoctorSchedule.as_view()), name='appoint_doctor'),
]
