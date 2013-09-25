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


class CheckPersonView(View):
    def post(self, request, *args, **kwargs):
        person_pk = request.POST.get('person_pk', None)
        date = request.POST.get('date', None)
        type_of = request.POST.get('type_of', None)
        if not type_of or not date or not person_pk:
            return HttpResponseBadRequest()

        person = get_object_or_404(Person, pk=person_pk)

        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        meal = get_object_or_404(Meal, date=date)

        if type_of == 'eat':
            # faça o processo para criação de um personmeal normal
            # person = get_object_or_404(Person, pk=person_pk)
            # meal = Meal.objects.get(date=date)
            # PersonMeal.objects.create(person=person, meal=meal)
            # mesmo processo do 'wash'
            person_meal, created = PersonMeal.objects.get_or_create(
                meal=meal,
                person=person,
                defaults={
                    'wash': False
                }
            )

        elif type_of == 'wash':
            PersonMeal.objects.filter(meal=meal, wash=True).update(wash=False)
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
        else:
            return HttpResponseBadRequest()

        meal_today = get_object_or_404(Meal, date=timezone.now().date())
        try:
            washer = meal_today.get_lowest_avg().name
        except AttributeError:
            washer = None
        return HttpResponse(
            json.dumps({
                'wash': True,
                'pk': person_meal.person.pk,
                'person_data': u'{} {}'.format(
                    person_meal.person.name,
                    person_meal.person.get_average(),
                ),
                'washer': washer,
            }),
            content_type='application/json'
        )
        # faça o processo de verificar se o personmeal desse pessoa já existe
        # se existe, setar o atributo wash como True e salvar
        # caso não exista, criar o personmeal da pessoa e setar o wash como true
        # retornar isso para o template

        # se o clique foi realizado no campo 'wash', verificar qual é a data
        # e verificar se a pessoa lavou naquele dia, caso tenha lavado,
        # mudar o status dela para 'não lavou', e vice-versa

class UncheckPersonView(View):
    def post(self, request, *args, **kwargs):
        person_pk = request.POST.get('person_pk', None)
        date = request.POST.get('date', None)
        type_of = request.POST.get('type_of', None)
        if not type_of or not date or not person_pk:
            raise HttpResponseBadRequest()

        person = get_object_or_404(Person, pk=person_pk)

        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        meal = get_object_or_404(Meal, date=date)

        pm = PersonMeal.objects.get(meal=meal, person=person)
        if type_of == 'eat':
            wash = False
            pm.delete()
        elif type_of == 'wash':
            wash = True
            pm.wash = False
            pm.save()
        else:
            raise HttpResponseBadRequest()
        try:
            pmn = pm.meal.get_lowest_avg().name
        except AttributeError:
                pmn = None
        return HttpResponse(
            json.dumps({
                'washer': pmn,
                'wash': wash
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
