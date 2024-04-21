from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Spam(models.Model) :
    phone_number = models.CharField(max_length = 10, validators = [MinLengthValidator(10), MaxLengthValidator(10)])
    spam_reported_count = models.IntegerField(null = True, blank = True) # Number of times the number is reported as a spam.

    def __str__(self) :
        return self.phone_number
