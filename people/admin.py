from django.contrib import admin
from people.models import Person

class PersonAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Person, PersonAdmin)
