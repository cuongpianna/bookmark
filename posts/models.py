from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="posts_created")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    users_like = models.ManyToManyField(get_user_model(),related_name="posts_liked",blank=True)


    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args,**kwargs)
