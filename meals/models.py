# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

from people.models import Person


class Meal(models.Model):
    date = models.DateField(unique=True)
    ordered = models.BooleanField(default=False)
    washer = models.ForeignKey('people.Person', null=True, blank=True)
    ticket = models.PositiveSmallIntegerField(null=True, blank=True)

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
