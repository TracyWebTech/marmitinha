# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

from people.models import Person


class Meal(models.Model):
    date = models.DateField()
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
