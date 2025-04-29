from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField

# Create your models here.

class CustomUser(AbstractUser):
    """Custom User Model"""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

class AboutMe(models.Model):
    """About Me model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about_me = HTMLField(blank=True, null=True, help_text='About me')
    image = models.ImageField(blank=True, null=False, upload_to='about_me/image')
    skills = models.ManyToManyField('Skill')
    my_name = models.CharField(max_length=100, help_text='Your name')
    social_media = models.JSONField(null=True, blank=True, help_text='Your social media link')

    def __str__(self): 
        return self.my_name 

class Education(models.Model):
    """Education model"""
    about_me = models.OneToOneField(AboutMe, on_delete=models.CASCADE)
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=4, help_text='Education Start date')
    end_year = models.CharField(max_length=4, help_text='Education End date')
    degree = models.CharField(max_length=100, help_text='Education Degree')
    university = models.CharField(max_length=100, help_text='Education University')
    description = HTMLField(help_text='Education Description')
    def __str__(self):
        return f"{self.degree} at {self.university}  ({self.start_year} - {self.end_year})"

class Experience(models.Model):
    """Experience model"""
    about_me = models.ForeignKey(AboutMe, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=4, help_text='Experience Start date')
    end_year = models.CharField(max_length=4, help_text='Experience End date')
    position = models.CharField(max_length=100, help_text='Experience position')
    company = models.CharField(max_length=100, help_text='Experience Company')
    description = HTMLField(help_text='Experience Description')

    def __str__(self):
        return f"{self.position} at {self.company} ({self.start_year} - {self.end_year})"

class Skill(models.Model):
    """Skill model"""
    name = models.CharField(max_length=100, unique=True, help_text="Enter your skill name")
    def __str__(self):
        return self.name

class Project(models.Model):
    """Project model"""
    title = models.CharField(max_length=100,  help_text='Project Title')
    year = models.DateField(max_length=4, help_text='Project Year')
    client = models.CharField(max_length=100, help_text='Project Client')
    service = models.CharField(max_length=100, help_text='Project Service')
    project_type = models.CharField(max_length=100, help_text='Project Type')
    description = HTMLField(help_text='Project Description')
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    """Project Image Model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='project_images/', help_text='Project Image')

    def __str__(self):
        return self.project.title

class YoutubeVideo(models.Model):
    """Youtube Video Model"""
    title = models.CharField(max_length=100, help_text='Youtube Video Title')
    link = models.URLField(help_text='Youtube Video Link')
    thumbnail = models.ImageField(upload_to="image/youtubethumbnail", help_text='Youtube Video Thumbnail')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.title
