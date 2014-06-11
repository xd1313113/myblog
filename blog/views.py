from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from blog.models import Post
from django.http import HttpResponse
# Create your views here.
def index(request):
#     posts = Post.objects.order_by('-created')
#     paginator = Paginator(posts, 10)
#     
#     try: page = int(request.GET.get("page", '1'))
#     except ValueError: page = 1
# 
#     try:
#         posts = paginator.page(page)
#     except (InvalidPage, EmptyPage):
#         posts = paginator.page(paginator.num_pages)
#     
    return render(request, 'blog/index.html')
#    return category(request,'project')

def category(request, type_id):
    posts = Post.objects.order_by('-created').all().filter(type=type_id)
    paginator = Paginator(posts, 10)
    
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/index.html', dict(posts=posts))

def post(request, post_id):
    return HttpResponse("You're looking at post %s."%post_id)

def resume(request):
    return render(request, 'blog/resume.html')

def about(request):
    return render(request, 'blog/about.html')