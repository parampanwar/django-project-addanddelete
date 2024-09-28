from django.db import models
from django_countries.fields import CountryField


class Hobby(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class User(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='NULL')
    country = CountryField(blank_label='(select country)', default='')
    email = models.EmailField()
    
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    choices = models.ManyToManyField(Hobby, blank=True)
    def __str__(self):
        return self.name
    


#code for importing file
class ExcelFile(models.Model):
    file=models.FileField(upload_to="excel")
    def __str__(self):
        return str(self.file)
    
    
