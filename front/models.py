from django.db import models

class CommDisaster(models.Model):
    Code=models.CharField(max_length=20)
    Date=models.CharField(max_length=32)
    Location=models.CharField(max_length=32)
    Type=models.CharField(max_length=32)
    SequenceNumber = models.CharField(max_length=32)
    Grade=models.IntegerField()
    Picture=models.CharField(max_length=200)
    Note=models.CharField(max_length=32)
    ReportingUnit=models.CharField(max_length=32)
