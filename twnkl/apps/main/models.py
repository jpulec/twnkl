from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

class Photo(models.Model):
    image = models.ImageField(upload_to="images/")
    owner = models.ForeignKey(User)
    group = models.ManyToManyField('PhotoGroup', blank=True)
    tags  = models.ManyToManyField('Tag', blank=True)
    loc   = GeopositionField(blank=True)

    def __unicode__(self):
        return str(self.owner) + ":" + str(self.tags) + ":" + str(self.group)

class Tag(models.Model):
    text = models.CharField(max_length=140)

    def __unicode__(self):
        return self.text

class PhotoGroup(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.user) + ":" + self.name
