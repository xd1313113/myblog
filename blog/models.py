from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from suit_ckeditor.widgets import CKEditorWidget
import os


# Create your models here.
class Post(models.Model):        
    """Post Model """
    author  = models.ForeignKey(User, null=True, blank=True)
    title   = models.CharField(max_length=60)
    excerpt = models.TextField(max_length=200)
    fulltext = models.TextField()
    image = models.ImageField(upload_to="images/")
    status  = models.CharField(max_length=20)
    created = models.DateTimeField()
    modified = models.DateTimeField()
    finished = models.DateTimeField()
    
    TYPE_OPTIONS = (('1','text'),('2','image'),('3','audio'),('4','video'),('5','project'))
    type    = models.CharField(max_length=1, choices=TYPE_OPTIONS)
    resource_link = models.TextField()
    
    def __unicode__(self):
        return self.title
    
    def thumbnail(self):
        return """<a href="/upload/%s"><img border="0" alt="" src="/images/%s" height="40" /></a>""" % (
                                                                    (self.image.name, self.image.name))
    
class Comment(models.Model):

    postID  = models.ForeignKey(Post, related_name="comments",  blank=True, null=True)
    content = models.TextField()
    author  = models.CharField(max_length=30)
    author_email    = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    status  = models.CharField(max_length=20)
    

    
    
    