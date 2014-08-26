from django.db import models

# Create your models here.
class Auftraggeber(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    members = models.ManyToManyField(Auftraggeber,through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    auftraggeber = models.ForeignKey(Auftraggeber)
    category = models.ForeignKey(Category)
