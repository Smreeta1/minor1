from django.db import models

# Create your models here.
# models.py


class citizen(models.Model):
    citizenship_no= models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    address=models.CharField(max_length=100)

    
class driver(models.Model):
    citizenship_no= models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
   
    
    


    def __str__(self):
       return self. name
