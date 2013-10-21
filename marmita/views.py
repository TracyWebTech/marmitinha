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
    people_who_ate = [person.person.pk for person in people_meal_filter]
    try:
        meal = Meal.objects.get(date=today)
    except Meal.DoesNotExist:
        meal = Meal.objects.create(date=today)

    ranking = Person.ranking()
    people = Person.objects.all()

    return render(request, 'index.html', {
        'people': people,
        'ranking': reversed(ranking),
        'min': meal.get_lowest_avg(),
        'form': AuthenticationForm,
        'today': today.strftime("%d/%m/%Y"),
        'pqc': people_who_ate,
        'who_wash': who_wash,
        'tickets': meal.ticket,
    })
