from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from photo.models import Image
from MySite.settings import MEDIA_URL

from time import strftime

# Create your views here.

def index(request):
    images = Image.objects.all()
    images = images.filter(featured=True)
    images = images.order_by('-created')
    
    paginator = Paginator(images, 10)
    
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        images = paginator.page(page)
    except (InvalidPage, EmptyPage):
        images = paginator.page(paginator.num_pages)
        
    for i, img in enumerate(images.object_list):
        img.created = img.created.strftime("%d %b")
        img.css_class = "featured hentry p"+str(i+1)+" post publish"
    
    return render(request, 'photo/index.html', dict(images=images,media_url = MEDIA_URL))

def single(request,image_id):
    image = Image.objects.get(id=image_id)
    if image:
        return render(request, 'photo/single.html',dict(image=image,media_url = MEDIA_URL))
    else:
        return '404'

def tag(request, tag_id):
    images = Image.objects.all().filter(tags__tag=tag_id)
    print len(images)
    for i, img in enumerate(images):
        img.created = img.created.strftime("%d %b")
        img.css_class = "featured hentry p"+str(i+1)+" post publish"
    if images:
        return render(request, 'photo/tag.html',dict(images=images,media_url = MEDIA_URL))
    