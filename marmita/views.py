import random
import datetime
import time

from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Max
from django.shortcuts import render

from people.models import Person
from meals.models import Meal, PersonMeal


def index(request):
    today = datetime.date.today()
    people_filter = PersonMeal.objects.filter(meal__date=today)
    pqc = [pm.pk for pm in people_filter]
    try:
        m = Meal.objects.get(date=today)
    except Meal.DoesNotExist:
        m = Meal.objects.create(date=today)
    ranking = list(Person.objects.all())
    ranking.sort(key=lambda x: x.get_average(), reverse=True)
    try:
        person_lower_average = ranking[-1]
    except IndexError:
        return render(request, 'index.html', {
            'people': [],
            'min': '',
            'form': AuthenticationForm,
        })
    people_copy = list(ranking)
    people_copy.pop()
    if not m.ordered and person_lower_average.get_average() \
            in [p.get_average() for p in people_copy]:
        draw = [person_lower_average,]
        for p in people_copy:
            if p.get_average() == person_lower_average.get_average():
                draw.append(p)
        person_lower_average = random.choice(draw)

    if not m.ordered:
        m.ordered = True
        m.washer = person_lower_average
        m.save()

    return render(request, 'index.html', {
        'people': ranking,
        'min': m.washer,
        'form': AuthenticationForm,
        'today': today.strftime("%d/%m/%Y"),
        'pqc': pqc,
    })
