from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='aga')
    date = models.DateField(verbose_name='date applied')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=150, default="Python Developer")
    application_amount = models.SmallIntegerField(default=1)
    localization = models.CharField(max_length=100, default='Wrocław')
    result = models.CharField(choices=[('accepted', 'accepted'), ('rejected','rejected'), ('under consideration', 'under consideration')], max_length=50, default='under consideration')

    def __str__(self):
        return self.company.name