from django.db import models

from accounts.models import MutsaUser

class CategoryChoices(models.TextChoices):
        IT = 'IT'
        SALES = '영업/고객상담'
        MANAGEMENT = '경영/사무'
        MARKETING = '마케팅/광고'
        PRODUCTION = '생산/제조'
        RESEARCH = '연구개발/설계'
        MEDICAL = '의료'
        TRADE = '무역/유통'
        CONSTRUCTION = '건설'
        SPECIALIST = '전문/특수직'
        DESIGN = '디자인'
        MEDIA = '미디어'
        ETC = '기타'

class Subject(models.Model):
    name = models.CharField(max_length=50, default='')
    category = models.CharField(choices=CategoryChoices.choices, max_length=7, blank=True)
    subject_detail = models.TextField()
    
class Votes(models.Model):
    mutsa_user = models.ForeignKey(MutsaUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)