from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employees'
    
    
