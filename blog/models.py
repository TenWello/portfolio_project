from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify, title
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='Category name')
    slug = models.SlugField(unique=True, max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__ (self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='Tag name e.g Django')
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__ (self):
        return self.name
class Blog(models.Model):
    """Blog Post Model"""
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('disabled', 'Disabled'),
    )
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=200, unique=True, help_text='Blog name')
    content = HTMLField(help_text='Blog Content')
    image = models.ImageField(upload_to='blog', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    comments_count = models.PositiveIntegerField(default=0, editable=False, help_text='Number of Comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blogs_post', blank=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', blank=True)
    tag = models.ManyToManyField(Tag, related_name='blogs', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.comments = None

    def update_comment_count(self):
        """Update the count of comments for this blog"""
        self.comments_count = self.comments.count()
        self.save()
        return self.comments_count

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Comment(models.Model):
    """Comment Model"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=200,  help_text='Comment name')
    email = models.EmailField(max_length=200, help_text='Comment email')
    message = HTMLField(help_text='Comment message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.email} ( {self.created_at} ) on {self.blog,title}"