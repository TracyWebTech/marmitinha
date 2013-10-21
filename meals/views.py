# -*- coding: utf-8 -*-

import datetime
import json

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from django.utils import timezone

from meals.models import Meal, PersonMeal
from people.models import Person


class CheckUncheckPersonView(View):
    def post(self, request, *args, **kwargs):
        check_uncheck = request.POST.get('check_uncheck', None)
        person_pk = request.POST.get('person_pk', None)
        date = request.POST.get('date', None)
        type_of = request.POST.get('type_of', None)
        if not type_of or not date or not person_pk:
            return HttpResponseBadRequest()

        person = get_object_or_404(Person, pk=person_pk)

        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        meal = get_object_or_404(Meal, date=date)

        if check_uncheck == 'uncheck_icon':
            if type_of == 'eat':
                person_meal, created = PersonMeal.objects.get_or_create(
                    meal=meal,
                    person=person,
                    defaults={
                        'wash': False
                    }
                )
                wash = False

            elif type_of == 'wash':
                person_meal, created = PersonMeal.objects.get_or_create(
                    meal=meal,
                    person=person,
                    defaults={
                        'wash': True
                    }
                )

                if not created:
                    person_meal.wash = True
                    person_meal.save()

                wash = True

            else:
                return HttpResponseBadRequest()

        elif check_uncheck == 'check_icon':
            person_meal = PersonMeal.objects.get(meal=meal, person=person)
            if type_of == 'eat':
                wash = False
                person_meal.delete()
            elif type_of == 'wash':
                wash = True
                person_meal.wash = False
                person_meal.save()
            else:
                raise HttpResponseBadRequest()

        else:
            return HttpResponseBadRequest()

        # The personal_data is used to rebuild the ranking with the changes
        # made changing the number of times people eat and washing the dishes
        personal_data = []
        ranking = [instance for instance in Person.ranking()]
        number_of_people = Person.objects.all().count()
        for person in ranking:
            personal_data.append([person.name, person.get_average(), person.weight, person.is_new, person.pk])

        meal_today = get_object_or_404(Meal, date=timezone.now().date())
        try:
            washer = meal_today.get_lowest_avg().name
        except AttributeError:
            washer = None

        number_of_meals = PersonMeal.objects.filter(meal=meal).count()

        return HttpResponse(
            json.dumps({
                'wash': wash,
                'pk': person_meal.person.pk,
                'person_data': list(reversed(personal_data)),
                'washer': washer,
                'number_of_people': number_of_people,
                'number_of_meals': number_of_meals,
            }),
            content_type='application/json'
        )

class ChangeDateView(View):
    def post(self, request, *args, **kwargs):
        date = request.POST.get('date', None)
        if not date:
            return HttpResponseBadRequest()

        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        try:
            meal = Meal.objects.get(date=date)
        except Meal.DoesNotExist:
            meal = Meal.objects.create(date=date)
        data = list(meal.personmeal_set.values_list('person__pk', 'wash'))
        data2 = {'tickets': meal.ticket, 'list': data}
        print data2
        print '***************************************************************'
        return HttpResponse(json.dumps(data2), content_type='application/json')


class ChangeTicketView(View):
    def post(self, request, *args, **kwargs):
        date = request.POST.get('date', None)
        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        meal = Meal.objects.get(date=date)
        meal.ticket = request.POST.get('ticket_num', None)
        meal.save()
        return HttpResponse()
