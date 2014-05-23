from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from string import join
import os
from PIL import Image as PImage
from MySite.settings import MEDIA_ROOT
from tempfile import *
from django.core.files import File

# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=60)
    public = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title

class Tag(models.Model):
    tag = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.tag


class Image(models.Model):
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True)
    albums = models.ManyToManyField(Album, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, blank=True)
    
    def __unicode__(self):
        return self.image.name
    
    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        im = PImage.open(os.path.join(MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        
#         # small thumbnail
#         fn, ext = os.path.splitext(self.image.name)
#         im.thumbnail((150,150), PImage.ANTIALIAS)
#         thumb_fn = fn + "-150x150" + ext
#         tf = NamedTemporaryFile()
#         im.save(tf.name, "JPEG")
#         self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
#         tf.close()  
#               
#         # large thumbnail
#         newheight = 300/self.width*self.height
#         im.thumbnail((300,newheight), PImage.ANTIALIAS)
#         thumb_fn = fn + "-300x"+ newheight + ext
#         tf2 = NamedTemporaryFile()
#         im.save(tf2.name, "JPEG")
#         self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
#         tf2.close()

        super(Image, self).save(*args, ** kwargs)

    def size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return str(join(lst, ', '))

    def albums_(self):
        lst = [x[1] for x in self.albums.values_list()]
        return str(join(lst, ', '))

    def thumbnail(self):
        return """<a href="/upload/%s"><img border="0" alt="" src="/images/%s" height="40" /></a>""" % (
                                                                    (self.image.name, self.image.name))
    thumbnail.allow_tags = True
    
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["title"]

class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__unicode__", "title", "user", "size", "tags_", "albums_",
        "thumbnail", "created"]
    list_filter = ["tags", "albums", "user"]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()