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


class requestList(models.Model):
    code = models.CharField(max_length=20)
    date = models.CharField(max_length=200)
    disasterType = models.CharField(max_length=4)
    status = models.IntegerField()
    o_URL = models.CharField(max_length=200)
    requestunit = models.CharField(max_length=50)

