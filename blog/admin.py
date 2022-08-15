from django.contrib import admin
from .models import BlogPost, PostReview, Tag

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(PostReview)
admin.site.register(Tag)