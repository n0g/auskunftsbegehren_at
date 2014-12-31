from django.db import models

# Create your models here.
class Auftraggeber(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.CharField(max_length=255)
    dvr = models.PositiveIntegerField(blank=True)
    comment = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class Application(models.Model):
    auftraggeber = models.ForeignKey(Auftraggeber)
    number = models.CharField(max_length=32)
    description = models.TextField()
    date = models.DateField()
    state = models.CharField(max_length=100)

    def __unicode__(self):
        return self.number + " " + self.description

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255,blank=True)
    members = models.ManyToManyField(Auftraggeber,through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    auftraggeber = models.ForeignKey(Auftraggeber)
    category = models.ForeignKey(Category)

class IdentityProof(models.Model):
    IDENTITY_CHOICES = (
        ('AUSWEIS', 'Kopie eines amtlichen Lichtbildausweises'),
        ('MELDEZETTEL', 'Kopie eines aktuellen Meldezettels'),
    )

    identity_proof = models.CharField(max_length=100, \
        choices=IDENTITY_CHOICES, default='AUSWEIS')

