from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView

from clients.forms import AddDoctorForm, AddManagerForm, AddAdminForm, AddCabinetForm, AddProcedureForm, \
    AddAppointmentForm
from clients.models import *


options = {
    'Співробітники': 'workers',
    'Пацієнти': 'users',
    'Записи': 'appointments',
    'Кабінети': 'cabinets',
    'Процедури': 'procedures'
}


def main(request):
    if Manager.objects.all().filter(name=request.user.username):
        context = {
            'options': options,
            'status': 'Менеджер',
            'is_manager': True if Manager.objects.all().filter(name=request.user.username) else False
        }
        return render(request, 'administrators/admin_main.html', context=context)
    if Administrator.objects.all().filter(name=request.user.username):
        context = {
            'options': options,
            'status': 'Адміністратор',
            'is_manager': True if Manager.objects.all().filter(name=request.user.username) else False
        }
        return render(request, 'administrators/admin_main.html', context=context)
    return redirect('home')


class WorkersTableView(ListView):
    model = ServiceWorkers
    template_name = 'administrators/tables/workers.html'
    context_object_name = 'workers'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'full_path': 'panel/workers',
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context


class UsersTableView(ListView):
    model = ServiceWorkers
    template_name = 'administrators/tables/users.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        users = User.objects.all()
        users = users.exclude(username__in=set(ServiceWorkers.objects.all().values_list('name', flat=True)))
        users = users.exclude(username__in=set(Manager.objects.all().values_list('name', flat=True)))
        users = users.exclude(username__in=set(Administrator.objects.all().values_list('name', flat=True)))

        context.update({
            'users': users,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context


class CabinetsTableView(ListView):
    model = Location
    template_name = 'administrators/tables/cabinets.html'
    context_object_name = 'cabinets'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'full_path': 'panel/cabinets',
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context


class AppointmentsTableView(ListView):
    model = Appointment
    template_name = 'administrators/tables/appointments.html'
    context_object_name = 'appointments'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'full_path': 'panel/appointments',
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False,
            'is_admin': True if Administrator.objects.all().filter(name=self.request.user.username) else False
        })

        return context


class ProceduresTableView(ListView):
    model = Procedure
    template_name = 'administrators/tables/procedures.html'
    context_object_name = 'procedures'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'full_path': 'panel/procedures',
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context


class CreateDoctor(CreateView):
    template_name = 'administrators/adding_templates/add_worker.html'
    model = ServiceWorkers
    success_url = "/panel/workers"
    form_class = AddDoctorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not Manager.objects.all().filter(name=request.user.username):
            return redirect('home')

        if form.is_valid():
            form.save()

            if len(Location.objects.filter(name_of_doctor='-')) > 0:
                last_doctor = ServiceWorkers.objects.all().order_by("-id")[0]
                last_doctor.location = Location.objects.filter(name_of_doctor='-')[0].cabinet_number
                cabinet = Location.objects.filter(name_of_doctor='-')[0]
                cabinet.name_of_doctor = last_doctor.name
                last_doctor.save()
                cabinet.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })


class CreateManager(CreateView):
    template_name = 'administrators/adding_templates/add_manager.html'
    model = Manager
    success_url = "/panel/workers"
    form_class = AddManagerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # if not Manager.objects.all().filter(name=request.user.username):
        #     return redirect('home')

        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })


class CreateAdmin(CreateView):
    template_name = 'administrators/adding_templates/add_admin.html'
    model = Administrator
    success_url = "/panel/workers"
    form_class = AddAdminForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not Manager.objects.all().filter(name=request.user.username):
            return redirect('home')

        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })


class CreateAppointment(CreateView):
    template_name = 'administrators/adding_templates/add_appointment.html'
    model = Manager
    success_url = "/panel/appointments"
    form_class = AddAppointmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not Administrator.objects.all().filter(name=request.user.username):
            return redirect('home')

        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })


class CreateCabinet(CreateView):
    template_name = 'administrators/adding_templates/add_cabinet.html'
    model = Location
    success_url = "/panel/cabinets"
    form_class = AddCabinetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not Manager.objects.all().filter(name=request.user.username):
            return redirect('home')

        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })


class CreateProcedure(CreateView):
    template_name = 'administrators/adding_templates/add_procedure.html'
    model = Procedure
    success_url = "/panel/procedures"
    form_class = AddProcedureForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'user': self.request.user,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not Manager.objects.all().filter(name=request.user.username):
            return redirect('home')

        if form.is_valid():
            form.save()

            return redirect(self.success_url)

        return render(request, self.template_name, {
            'form': form,
            'options': options,
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })


class ShowDoctor(DetailView):
    model = ServiceWorkers
    template_name = 'administrators/doctor.html'
    pk_url_kwarg = 'doctor_id'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = ServiceWorkers.objects.filter(id=self.kwargs['doctor_id'])[0]

        context.update({
            'user': self.request.user,
            # 'procedures': Procedure.objects.filter(name_of_speciality=doctor.speciality),
            'doctor': ServiceWorkers.objects.filter(id=self.kwargs['doctor_id'])[0],
            'ap_amount': len(Appointment.objects.filter(name_of_doctor=doctor.name)),
            'is_manager': True if Manager.objects.all().filter(name=self.request.user.username) else False
        })
        return context


def delete_appointment(request):
    ap_id = request.POST.get('post_id')
    Appointment.objects.filter(id=ap_id).delete()

    return JsonResponse({'data': '', 'csrfmiddlewaretoken': request.POST.get('csrfmiddlewaretoken')})
