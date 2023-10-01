from django.db import models


class Tools(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + " " + self.description


class SeedInventory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name + " " + self.description

class Inventory(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.name + " " + str(self.amount)

class Money(models.Model):
    amount = models.IntegerField()
    
    def __str__(self):
        return str(self.amount) + " gold"