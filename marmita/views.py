# -*- coding: utf-8 -*-

import datetime
# import random
# import time

from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Max
from django.shortcuts import render

from meals.models import Meal, PersonMeal
from people.models import Person


def index(request):
    today = datetime.date.today()
    people_meal_filter = PersonMeal.objects.filter(meal__date=today)
    try:
        who_wash = people_meal_filter.get(wash=True).person
    except PersonMeal.DoesNotExist:
        who_wash = None
    pqc = [pm.person.pk for pm in people_meal_filter]
    try:
        m = Meal.objects.get(date=today)
    except Meal.DoesNotExist:
        m = Meal.objects.create(date=today)
    
    ranking = list(Person.objects.all())
    ranking.sort(key=lambda x: x.get_average(), reverse=True)

    return render(request, 'index.html', {
        'people': ranking,
        'min': m.get_lowest_avg(),
        'form': AuthenticationForm,
        'today': today.strftime("%d/%m/%Y"),
        'pqc': pqc,
        'who_wash': who_wash,
        'tickets': m.ticket,
    })
