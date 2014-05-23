from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Posts(models.Model):
    #id      = models.BigIntegerField()
    author  = models.ForeignKey(User, null=True, blank=True)
    title   = models.CharField(max_length=60)
    excerpt = models.TextField(max_length=200)
    content = models.TextField()
    status  = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(auto_now_add=True)
    
    TYPE_OPTIONS = (('1','text'),('2','image'),('3','audio'),('4','video'),('5','project'))
    type    = models.CharField(max_length=1, choices=TYPE_OPTIONS)
    resource_link = models.TextField()
    
    
    
class Comments(models.Model):
    #id      = models.BigIntegerField()
    postID  = models.ForeignKey(Posts, related_name="comments",  blank=True, null=True)
    content = models.TextField()
    author  = models.CharField(max_length=30)
    author_email    = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    status  = models.CharField(max_length=20)
    
    
    