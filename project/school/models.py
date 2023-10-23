from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid 


# Create your models here.
class User(AbstractUser):
    id = models.CharField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False, 
         max_length=180) 
    A = models.IntegerField(default=10)
    B = models.IntegerField(default=10)
    C = models.IntegerField(default=10)
    D = models.IntegerField(default=10)
    E = models.IntegerField(default=10)
    F = models.IntegerField(default=10)
    G = models.IntegerField(default=10)
    H = models.IntegerField(default=10)
    I = models.IntegerField(default=10)

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=120)
    is_error = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now)
    user_name = models.CharField(max_length=160)
    error = models.CharField(max_length=120, null=True, default=None)
    



