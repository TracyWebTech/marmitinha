# -*- coding: utf-8 -*-

import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View

from meals.models import Meal, PersonMeal
from people.models import Person


def create_person_meal_with_wash(meal, person, pm=None, has_pm=False):
    try:
        pw = PersonMeal.objects.get(meal=meal, wash=True)
    except PersonMeal.DoesNotExist:
        if has_pm and pm:
            pm.wash = True
            pm.save()
            return pm
        return PersonMeal.objects.create(meal=meal, person=person, wash=True)
    else:
        pw.wash = False
        pw.save()
    if has_pm and pm:
        pm.wash = True
        pm.save()
        return pm
    return PersonMeal.objects.create(meal=meal, person=person, wash=True)



class CheckPersonView(View):
    def post(self, request, *args, **kwargs):
        person_pk = request.POST.get('person_pk', None)
        date = request.POST.get('date', None)
        type_of = request.POST.get('type_of', None)
        if not type_of or not date or not person_pk:
            raise HttpResponseBadRequest()

        person = get_object_or_404(Person, pk=person_pk)

        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        meal = get_object_or_404(Meal, date=date)

        if type_of == 'eat':
            # faça o processo para criação de um personmeal normal
            # person = get_object_or_404(Person, pk=person_pk)
            # meal = Meal.objects.get(date=date)
            # PersonMeal.objects.create(person=person, meal=meal)
            # mesmo processo do 'wash'
            try:
                pm = PersonMeal.objects.get(meal=meal, person=person)
            except PersonMeal.DoesNotExist:
                pm = PersonMeal.objects.create(meal=meal, person=person)
            finally:
                return HttpResponse()

        elif type_of == 'wash':
            try:
                pw = PersonMeal.objects.get(meal=meal, person=person)
            except PersonMeal.DoesNotExist:
                pw = create_person_meal_with_wash(meal, person)
            else:
                create_person_meal_with_wash(meal, person, pw, has_pm=True)
            return HttpResponse(u'wash')
            # faça o processo de verificar se o personmeal desse pessoa já existe
            # se existe, setar o atributo wash como True e salvar
            # caso não exista, criar o personmeal da pessoa e setar o wash como true
            # retornar isso para o template

            # se o clique foi realizado no campo 'wash', verificar qual é a data
            # e verificar se a pessoa lavou naquele dia, caso tenha lavado,
            # mudar o status dela para 'não lavou', e vice-versa
        else:
            pass
            # levante uma exceção
