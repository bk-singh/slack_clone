from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Comments(models.Model):
	user = models.ForeignKey(User)
	text = models.CharField(max_length=255)
	channel = models.CharField(max_length=50)