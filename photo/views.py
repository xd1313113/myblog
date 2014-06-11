from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
from django import template
from django.contrib.sites.models import Site

from time import strftime
from datetime import datetime
import flickr


# Create your views here.
images_list = []
flickrapi = flickr.Flickr(settings.FLICKR_API_KEY)
register = template.Library()

def get_site(parser, token):
    return Site.objects.get_current().domain

register.tag('site_url', get_site)



def index(request):
    global images_list,site
    if not images_list:
        images_list = flickrapi.search(user_id="123556379@N06")
    
    paginator = Paginator(images_list, 10)
    
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        images = paginator.page(page)
    except (InvalidPage, EmptyPage):
        images = paginator.page(paginator.num_pages)
        
    for i, img in enumerate(images.object_list):
        img = flickrapi.getImageInfo(img.id, img)
        img.created = datetime(int(img.taken[:4]),int(img.taken[5:7]),int(img.taken[8:10]))
        #img.created = img.created.strftime("%d %b")
        img.css_class = "featured hentry p"+str(i+1)+" post publish"
        img.url_z = img.get_pic_url('z')
    return render(request, 'photo/index.html', dict(images=images))

def single(request,image_id):
    global images_list
    
    if not images_list:
        images_list = flickrapi.search(user_id="123556379@N06")
        
    for img in images_list:
        if img.id == image_id:
            img = flickrapi.getImageInfo(img.id, img)
            img.url_o = img.get_pic_url('o')
            image = img
    
    if image:
        return render(request, 'photo/single.html',dict(image=image))
    else:
        return '404'

def tag(request, tag_id):
    tag_images = flickrapi.search(user_id="123556379@N06",tags=tag_id)
    
    paginator = Paginator(tag_images, 5)
    
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        images = paginator.page(page)
    except (InvalidPage, EmptyPage):
        images = paginator.page(paginator.num_pages)
        
    for i, img in enumerate(images.object_list):
        img = flickrapi.getImageInfo(img.id, img)
        img.created = datetime(int(img.taken[:4]),int(img.taken[5:7]),int(img.taken[8:10]))
        #img.created = img.created.strftime("%d %b")
        img.css_class = "featured hentry p"+str(i+1)+" post publish"
        img.url_z = img.get_pic_url('z')
    return render(request, 'photo/tag.html', dict(images=images, tag = tag_id))