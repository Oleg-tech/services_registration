from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=255, verbose_name="Прізвище Ім'я")
    registrations = models.IntegerField(default=0, null=0, verbose_name="Прізвище Ім'я")


class Administrator(models.Model):
    name = models.CharField(max_length=255, verbose_name="Прізвище Ім'я")
    registrations = models.IntegerField(default=0, null=0, verbose_name="Прізвище Ім'я")


class ServiceWorkers(models.Model):
    name = models.CharField(max_length=255, verbose_name="Прізвище Ім'я")
    location = models.CharField(max_length=255, default='-', null='-', verbose_name="Місце роботи")
    speciality = models.CharField(max_length=20, verbose_name="Спеціальність")
    schedule_from = models.CharField(max_length=30, verbose_name="Розклад від")
    schedule_to = models.CharField(max_length=30, verbose_name="Розклад до")


class Location(models.Model):
    cabinet_number = models.IntegerField(verbose_name="Номер кабінету")
    name_of_doctor = models.CharField(max_length=255, default='-', null='-', verbose_name="Ім'я лікаря")


class Appointment(models.Model):
    name_of_patient = models.CharField(max_length=255, default='-', null='-', verbose_name="Ім'я пацієнта")
    name_of_doctor = models.CharField(max_length=255, default='-', null='-', verbose_name="Ім'я лікаря")
    name_of_procedure = models.CharField(max_length=255, verbose_name="Назва процедури")

    day = models.IntegerField(default=0, null=0, verbose_name="День")
    hour = models.IntegerField(verbose_name="Година")


class Procedure(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва процедури")
    name_of_speciality = models.CharField(max_length=255, default='-', null='-', verbose_name="Ім'я лікаря")
    duration = models.IntegerField(verbose_name="Тривалість")
