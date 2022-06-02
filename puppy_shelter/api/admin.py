from django.contrib import admin
from api import models


@admin.register(models.Adopter)
class AdopterAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Puppy)
class PuppyAdmin(admin.ModelAdmin):
    pass
