# -*- coding: utf-8 -*-

import random

from django.db import models
from django.core.exceptions import ValidationError

from people.models import Person


class Meal(models.Model):
    date = models.DateField(unique=True)
    ordered = models.BooleanField(default=False)
    washer = models.ForeignKey('people.Person', null=True, blank=True)
    ticket = models.PositiveSmallIntegerField(null=True, blank=True)

    def washer_of_today(self):
        who_ate = [p.person for p in self.personmeal_set.all()]

        if not who_ate and not self.washer:
            return self.get_lowest_avg()
        elif not who_ate and self.washer:
            return self.washer

        the_washer = None
        new_member = self.personmeal_set.filter(person__is_new=True)
        if new_member:
            if new_member.count() > 1:
                the_washer = random.choice(list(new_member)).person
            else:
                the_washer = new_member[0].person
        if not the_washer:
            the_washer = self.get_lowest_avg()
        if not self.ordered and not the_washer.is_new and \
            the_washer.get_average() in [p.get_average() \
                    for p in who_ate]:
            draw = []
            for p in who_ate:
                if p.get_average() == the_washer.get_average():
                    draw.append(p)
            the_washer = random.choice(draw)

        self.washer = the_washer
        if not self.ordered:
            self.ordered = True

        self.save()

        return self.washer

    def get_lowest_avg(self):
        people = list(Person.objects.all())
        people.sort(key=lambda x: x.get_average(), reverse=True)
        try:
            return people[-1]
        except IndexError:
            return None

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
        if self.person.is_new and self.wash:
            n_wash = self.person.personmeal_set.filter(wash=True)
            n_people = Person.objects.exclude(pk=self.person.pk)
            if n_wash.count() == n_people.count():
                for wash in n_wash:
                    wash.wash = False
                    wash.save()
                self.person.is_new = False
                self.person.save()
        super(PersonMeal, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.wash:
            pm = self.meal.personmeal_set.filter(wash=True)
            if self.pk:
                pm = pm.exclude(pk=self.pk)
            if pm.exists():
                raise ValidationError('Não pode fiote')
        super(PersonMeal, self).save(*args, **kwargs)
