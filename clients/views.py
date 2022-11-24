import datetime

from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView

from .forms import *


class AdminLoginView(View):
    template_name = 'clients/login.html'
    success_url = reverse_lazy('home')
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('username'))
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
            )

            if user is not None:
                login(request, user)
                return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


def user_exit(request):
    logout(request)
    return redirect('home')


class CreateUser(CreateView):
    template_name = 'clients/registration.html'
    model = User
    success_url = "/"
    form_class = CreateUserForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


def check_if_worker(user):
    is_admin = True if len(Manager.objects.filter(name=user.username)) != 0 else False
    is_manager = True if len(Administrator.objects.filter(name=user.username)) != 0 else False
    return True if is_admin or is_manager == True else False


def check_if_doctor(user):
    return True if len(ServiceWorkers.objects.filter(name=user.username)) != 0 else False


def main_page_clients(request):
    context = {
        'user': request.user,
    }

    if not request.user.is_anonymous:
        context = {
            'user': request.user,
            'is_worker': check_if_worker(request.user),
            'is_doctor': check_if_doctor(request.user)
        }

    return render(request, 'clients/main.html', context=context)


def make_appointment(request):
    context = {
        'user': request.user,
        'professions': set(ServiceWorkers.objects.values_list('speciality', flat=True)),
        'doctors': ServiceWorkers.objects.all()
    }
    if not request.user.is_anonymous:

        context = {
            'user': request.user,
            'is_worker': check_if_worker(request.user),
            'is_doctor': check_if_doctor(request.user),
            'professions': set(ServiceWorkers.objects.values_list('speciality', flat=True)),
            'doctors': ServiceWorkers.objects.all()
        }

    return render(request, 'clients/make_appointment.html', context=context)


def filter_data(request):
    selected_specialities = request.GET.getlist('speciality[]')

    list_of_specialists = ServiceWorkers.objects.all()
    if len(selected_specialities) > 0:
        list_of_specialists = list_of_specialists.filter(speciality__in=selected_specialities)

    filtered_part = render_to_string('clients/ajax_templates/make_appointment.html', {
        'doctors': list_of_specialists
    })

    return JsonResponse({
        'data': filtered_part
    })


def get_working_hours(work_from, work_to, doctor):
    hours = {}
    for hour in range(0, work_from):
        hours[hour+1] = 'inactive'
    for hour in range(work_from, work_to):
        hours[hour] = 'active'
    for hour in range(work_to, 24):
        hours[hour] = 'inactive'

    for i in Appointment.objects.filter(name_of_doctor=doctor.name):
        for j in range(Procedure.objects.get(name=i.name_of_procedure).duration):
            print(i.hour+j)
            hours[i.hour+j] = 'inactive'

    return hours


class CreateProcedure(CreateView):
    model = Procedure
    template_name = 'clients/add_procedure.html'
    context_object_name = 'object'
    form_class = CreateUserForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


def check_time(point_hour, duration, doctor):
    hours = get_working_hours(int(doctor.schedule_from), int(doctor.schedule_to), doctor)
    for i in range(duration):
        if hours[point_hour+i] == 'inactive':
            return False
    return True


class ShowDoctorSchedule(DetailView):
    model = ServiceWorkers
    template_name = 'clients/choose_time.html'
    pk_url_kwarg = 'doctor_id'
    context_object_name = 'object'
    form_class = AddAppointmentForm
    success_url = '/make_appointment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.success_url = '/make_appointment'

        work_from = ServiceWorkers.objects.values_list('schedule_from', flat=True).get(id=self.kwargs['doctor_id'])
        work_to = ServiceWorkers.objects.values_list('schedule_to', flat=True).get(id=self.kwargs['doctor_id'])
        doctor = ServiceWorkers.objects.get(id=self.kwargs['doctor_id'])
        context.update({
            'user': self.request.user,
            'hours': get_working_hours(int(work_from), int(work_to), ServiceWorkers.objects.get(id=self.kwargs['doctor_id'])),
            'procedures': Procedure.objects.all().filter(name_of_speciality=doctor.speciality),
            'form': self.form_class,
            'is_worker': check_if_worker(self.request.user),
            'is_doctor': check_if_doctor(self.request.user)
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            spec = ServiceWorkers.objects.get(id=self.kwargs['doctor_id']).speciality

            added_procs = Procedure.objects.filter(name_of_speciality=spec)

            added_procs = added_procs.filter(name=form.cleaned_data.get('name_of_procedure'))
            if len(added_procs) > 0:
                if check_time(
                                form.cleaned_data.get('hour'),
                                added_procs[0].duration,
                                ServiceWorkers.objects.get(id=self.kwargs['doctor_id'])
                            ):

                    form.save()

                    last_appointment = Appointment.objects.all().order_by("-id")[0]
                    last_appointment.name_of_patient = self.request.user.username
                    last_appointment.name_of_doctor = ServiceWorkers.objects.get(id=self.kwargs['doctor_id']).name
                    last_appointment.day = int(datetime.datetime.now().strftime("%d"))+1
                    last_appointment.save()

                    return redirect(self.success_url)

        work_from = ServiceWorkers.objects.values_list('schedule_from', flat=True).get(id=self.kwargs['doctor_id'])
        work_to = ServiceWorkers.objects.values_list('schedule_to', flat=True).get(id=self.kwargs['doctor_id'])
        doctor = ServiceWorkers.objects.get(id=self.kwargs['doctor_id'])

        return render(request, self.template_name, {
            'user': self.request.user,
            'hours': get_working_hours(int(work_from), int(work_to), ServiceWorkers.objects.get(id=self.kwargs['doctor_id'])),
            'procedures': Procedure.objects.all().filter(name_of_speciality=doctor.speciality),
            'form': self.form_class,
            'is_worker': check_if_worker(self.request.user),
            'is_doctor': check_if_doctor(self.request.user)
        })


def my_appointments(request):
    context = {
        'appointments': Appointment.objects.filter(name_of_patient=request.user.username),
        'is_worker': check_if_worker(request.user),
        'is_doctor': check_if_doctor(request.user)
    }
    return render(request, 'clients/my_appointments.html', context=context)


def delete_appointment(request):
    if not Administrator.objects.filter(name=request.user.username):
        redirect('home')

    ap_id = request.POST.get('post_id')
    Appointment.objects.filter(id=ap_id).delete()

    return JsonResponse({'data': '', 'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken')})
