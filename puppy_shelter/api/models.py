from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Adopter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=9)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f'''
        Adopter(
            first_name={self.first_name},
            last_name={self.last_name},
            city={self.city},
            phone={self.phone}
        )
        '''


class Adoption(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    adopter = models.ForeignKey(Adopter, on_delete=models.CASCADE)
    adoption_date_utc = models.DateTimeField(default=datetime.utcnow)

    def __str__(self) -> str:
        return f'''
        Adoption(
            adopter={self.adopter}
        )
        '''


class Puppy(models.Model):
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    def __str__(self) -> str:
        return f'''
        Puppy(
            name={self.name},
            adoption={self.adoption}
        )
        '''
