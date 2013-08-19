from django.db import models

class Meal(models.Model):                                                    
    date = models.DateField()
    
    def __unicode__(self):
        return unicode(self.date)

class PersonMeal(models.Model):
    person = models.ForeignKey('people.Person')
    meal = models.ForeignKey('Meal')
    wash = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('person', 'meal', 'wash')
    
