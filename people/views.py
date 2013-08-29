# -*- coding: utf-8 -*-

import datetime
import json

from django.http import HttpResponse
from django.views.generic import View

from meals.models import Meal
from .forms import PersonCreateForm
from .models import Person


class CreatePersonView(View):
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', None)
        if not name:
            return HttpResponse(u'Não foi possível criar a pessoa')
        new_person = Person.objects.create(name=name)
        today = datetime.date.today()
        try:
            meal = Meal.objects.get(date=today)
            meal.washer = new_person
            meal.save()
        except Meal.DoesNotExist():
            Meal.objects.create(date=today, ordered=True, washer=new_person)
        return HttpResponse(unicode(new_person.name))
