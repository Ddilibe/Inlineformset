from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Article(models.Model):
    state = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    status = models.CharField(max_length=11, choices=state, default="draft")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager() 
    published = PublishedManager() 
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('Article:Article_list', kwargs={"pk": self.pk})
        
class Add_image(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.article.title
        
class Add_body(models.Model):
    body = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.article.title
        
class Add_video(models.Model):
    video = models.FileField(upload_to='video/')
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.article.title
        
        

