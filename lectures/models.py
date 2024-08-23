from django.db import models

from subjects.models import CategoryChoices, Subject
from accounts.models import MutsaUser

# Create your models here.

class Lecture(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    mutsa_user = models.ForeignKey(MutsaUser, on_delete=models.CASCADE)
    title = models.CharField(default='')
    category = models.CharField(choices=CategoryChoices.choices, max_length=1, blank=True)
    cost = models.IntegerField()
    min_total_cost = models.IntegerField()
    max_student = models.IntegerField()
    lecture_detail = models.TextField()
    
class Fundings(models.Model):
    mutsa_user = models.ForeignKey(MutsaUser, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)