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

    # person_lower_average = ''
    # new_member = Person.objects.filter(is_new=True)
    # if new_member:
    #     if new_member.count() > 1:
    #         person_lower_average = random.choice(list(new_member))
    #     else:
    #         person_lower_average = new_member[0]

    ranking = list(Person.objects.all())
    ranking.sort(key=lambda x: x.get_average(), reverse=True)

    # try:
    #     if not person_lower_average:
    #         person_lower_average = m.get_lowest_avg()
    # except IndexError:
    #     return render(request, 'index.html', {
    #         'people': [],
    #         'min': '',
    #         'form': AuthenticationForm,
    #         'today': today.strftime("%d/%m/%Y"),
    #         'pqc': [],
    #         'who_wash': None,
    #     })
    # people_copy = list(ranking)
    # people_copy.pop()
    # if not m.ordered and not person_lower_average.is_new and \
    #         person_lower_average.get_average() in [p.get_average() \
    #                 for p in people_copy]:
    #     draw = [person_lower_average,]
    #     for p in people_copy:
    #         if p.get_average() == person_lower_average.get_average():
    #             draw.append(p)
    #     person_lower_average = random.choice(draw)

    # if not m.ordered:
    #     m.ordered = True
    #     m.washer = person_lower_average
    #     m.save()

    return render(request, 'index.html', {
        'people': ranking,
        'min': m.washer_of_today(),
        'form': AuthenticationForm,
        'today': today.strftime("%d/%m/%Y"),
        'pqc': pqc,
        'who_wash': who_wash,
    })
