from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

# app_name = 'panel'

urlpatterns = [
    path('main/', login_required(main), name='main_admin'),

    # show
    path('workers/', login_required(WorkersTableView.as_view()), name='workers'),
    path('users/', login_required(UsersTableView.as_view()), name='users'),
    path('cabinets/', login_required(CabinetsTableView.as_view()), name='cabinets'),
    path('appointments/', login_required(AppointmentsTableView.as_view()), name='appointments'),
    path('doctor_info/<str:doctor_id>/', login_required(ShowDoctor.as_view()), name='show_doctor'),
    path('procedures/', login_required(ProceduresTableView.as_view()), name='procedures'),

    # add
    path('add_worker/', login_required(CreateDoctor.as_view()), name='add_worker'),
    path('add_manager/', CreateManager.as_view(), name='add_manager'),
    path('add_admin/', login_required(CreateAdmin.as_view()), name='add_admin'),
    path('add_appointment/', login_required(CreateAppointment.as_view()), name='add_appointment'),
    path('add_cabinet/', login_required(CreateCabinet.as_view()), name='add_cabinet'),
    path('add_procedure/', login_required(CreateProcedure.as_view()), name='add_procedure'),

    # ajax
    path('delete_appointment/', login_required(delete_appointment), name='delete_appointment'),
]
