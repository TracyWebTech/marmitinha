from django.contrib import admin
from meals.models import PersonMeal, Meal

class PersonMealInline(admin.TabularInline):
    model = PersonMeal


class MealAdmin(admin.ModelAdmin):
    inlines = [PersonMealInline]

admin.site.register(Meal, MealAdmin)
