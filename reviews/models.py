from django.db import models

from accounts.models import MutsaUser
from lectures.models import Lecture

# Create your models here.

class Review(models.Model):
    mutsa_user = models.ForeignKey(MutsaUser, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    content = models.TextField()