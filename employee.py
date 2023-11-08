from django.db import models

class Employees(models.Model):
    username = models.CharField(max_length=200)
    age = models.IntegerField()

    def __str__(self):
        return self.username
