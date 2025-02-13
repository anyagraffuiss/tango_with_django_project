from django.db import models
from django.contrib.auth.models import User


# model representing a category of pages
class Category(models.Model):
    name = models.CharField(max_length=128, unique = True)

    def __str__(self):
        return self.name
# model representing an individual page    
class Page(models.Model):
    # link to a specific category
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    # page title
    title = models.CharField(max_length = 128)
    # page URL
    url = models.URLField()
    # number of views the page has recieved
    views = models.IntegerField(default = 0)

    def __str__(self):
        return self.title
    
# model representing a user profile    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username