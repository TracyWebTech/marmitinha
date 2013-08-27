# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

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
