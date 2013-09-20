from django.db import models
from django.contrib.auth.models import User
from geoposition.fields import GeopositionField

import os

class Photo(models.Model):
    image = models.ImageField(upload_to="images/")
    name  = models.CharField(max_length=256)
    owner = models.ForeignKey(User)
    groups= models.ManyToManyField('PhotoGroup')
    tags  = models.ManyToManyField('Tag', blank=True)
    loc   = GeopositionField(blank=True)
    dt    = models.DateTimeField(auto_now_add=True)

    def get_first_group(self):
        return self.groups[0].name

    def safe_filename(self):
        return os.path.splitext(os.path.basename(self.image.name))[0]

    def __unicode__(self):
        return str(self.owner) + ":" + str(self.tags) + ":" + str(self.groups)



class Tag(models.Model):
    text = models.CharField(max_length=140)

    def __unicode__(self):
        return self.text

class PhotoGroup(models.Model):
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.owner) + ":" + self.name
