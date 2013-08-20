from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=70)

    def count_wash(self):
        #countwash = PersonMeal.objects.filter(wash=True, person=self).count()
        #nesse caso seria preciso importar PersonMeal
        countwash = Person.personmeal_set.filter(wash=True).count()
        return countwash

    def __unicode__(self):
        return self.name
