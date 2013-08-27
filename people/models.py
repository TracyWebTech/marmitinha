from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=70)

    def count_wash(self):
        #countwash = PersonMeal.objects.filter(wash=True, person=self).count()
        #nesse caso seria preciso importar PersonMeal
        return self.personmeal_set.filter(wash=True).count()

    def count_eat(self):
        # PersonMeal.object.filter(person=self).count()
        return self.personmeal_set.count()

    def get_average(self):
        eat = self.count_eat()
        if not eat:
            return 0.0
        return round(float(self.count_wash())/self.count_eat(), 3)

   #def maximum(self):
   #    return self.objects.all().get(Max('get_average()'))

    def __unicode__(self):
        return self.name
