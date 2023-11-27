from django.db import models

class Blog(models.Model):
    account_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    url = models.CharField(max_length=100)