# -*- coding: utf-8 -*-

import random
import datetime

from django.db import models
from django.core.exceptions import ValidationError

from people.models import Person


class Meal(models.Model):
    date = models.DateField(unique=True)
    ordered = models.BooleanField(default=False)
    washer = models.ForeignKey('people.Person', null=True, blank=True)
    ticket = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def _create_random(cls, meal):
        if meal.ordered:
            return False
        people = list(Person.objects.all())
        random.shuffle(people)
        for i, person in enumerate(people):
            person.weight = i
            person.save()
        meal.ordered = True

    def __init__(self, *args, **kwargs):
        super(Meal, self).__init__(*args, **kwargs)
        if self.date == datetime.date.today():
            Meal._create_random(self)

    def get_lowest_avg(self):
        ranking = Person.ranking()
        wash = None
        for person in ranking:
            if person.personmeal_set.filter(meal=self).exists():
                if person.is_new:
                    return person
                elif person.get_average() != unicode(0.0):
                    return person
                if not wash:
                    wash = person
        return wash

    def __unicode__(self):
        return unicode(self.date)

class PersonMeal(models.Model):
    person = models.ForeignKey('people.Person')
    meal = models.ForeignKey('Meal')
    wash = models.BooleanField(default=False)

    class Meta:
        unique_together = (('person', 'meal'),)

    def __unicode__(self):
        return u'{} - ({})'.format(self.person.name, self.meal.date)

    def save(self, *args, **kwargs):
        if self.wash:
            PersonMeal.objects.filter(meal=self.meal, wash=True).update(wash=False)

            if self.person.is_new:
                n_wash = self.person.personmeal_set.filter(wash=True)
                n_people = Person.objects.exclude(pk=self.person.pk)
                if n_wash.count() >= n_people.count():
                    for wash in n_wash:
                        wash.wash = False
                        wash.save()
                    self.person.is_new = False
                    self.person.save()
        super(PersonMeal, self).save(*args, **kwargs)
