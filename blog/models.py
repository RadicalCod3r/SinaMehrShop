from django.db import models
from users.models import User

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='images/blog', default='images/blog/sample_blog.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    
    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class PostReview(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_reviews')
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=50, default='کاربر جدید')
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} commented on {self.blog_post.title}'
    