from django.contrib import admin

# Register your models here.
from blog.models import Post
from django.forms import ModelForm
from suit_ckeditor.widgets import CKEditorWidget
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea

class PostForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'excerpt': AutosizedTextarea(attrs={'rows': 2}),
            'resource_link': AutosizedTextarea(attrs={'rows': 3}),
            'created': SuitSplitDateTimeWidget,
            'modified': SuitSplitDateTimeWidget,
            'finished': SuitSplitDateTimeWidget,
            'fulltext': CKEditorWidget()
        }    
        

class PostAdmin(admin.ModelAdmin):
    form = PostForm 
    search_fields = ["title"]
    fieldsets = [
        ('New Post', {'fields': ['title', 'author','excerpt','status','type','resource_link']}),         
        
        ('Dates', {'classes': ('collapse', 'open'),
                   'fields': ['created','modified','finished']}),
        ('Edit Post', {
        'classes': ('full-width',),
        'description': 'Edit Posts',
        'fields': ['fulltext']}),
                 
        ('Thumbnail', {'fields': ['image']})
    ]
    list_display = ["__unicode__","title","author",  "excerpt","type", "status", "image", "created","finished"]
    list_filter = ["title", "status", "author"]
        
admin.site.register(Post,PostAdmin)