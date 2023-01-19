from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.



class Post(models.Model):
    
    choice = {
        ('published','published'),
        ('draft', 'draft')
    }
    
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default='Arabian Nights Safari Blogs')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body   = RichTextField(blank=True, null=True)
    post_created = models.DateTimeField(auto_now_add=True)
    post_updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(null=True, blank=True, default='/static/images/img/blog-1.jpg')
    likes = models.ManyToManyField(User, related_name='blog_posts')
    status = models.CharField(choices=choice, max_length=50, default="published")


    @property
    def total_likes(self):
        return self.likes.all().count()
    
    def __str__(self):
        return self.title + ' | ' +  str(self.author)

    def get_absolute_url(self):
        return reverse("post-detail", args=(str(self.id)))
        
    
    


LIKE_CHOICES = (
    ('Like', 'Like'), 
     ('Unlike', 'Unlike')
)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=LIKE_CHOICES, default='Unlike')
    
    
    
    
    def __str__(self):
        return f'{self.post} -  {self.user}'
    
    


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name =  models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)