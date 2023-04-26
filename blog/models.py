from django.db import models
import uuid
from accounts.models import User
from autoslug import AutoSlugField
from django.utils.text import slugify 
from announcement.models import Announcement

class Tag(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return f'Tag[id: {self.uid}, name: {self.tag_name}]'


class Blog(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name= "blogs")
    blog_title = models.CharField(max_length=500 , blank=True)
    blog_text = models.TextField(blank=True)
    json_data = models.JSONField(default= dict , null=True , blank=True)
    # main_image = models.ImageField(upload_to="blogs_image" , null=True , blank= True)
    main_image_64 = models.TextField(null=True, blank=True)
    # slug = AutoSlugField(populate_from='blog_title' , unique = True )
    slug = models.SlugField(default='',editable=False, null=True,blank=True,max_length=250) 
    tags = models.ManyToManyField(Tag, related_name='TaggedModel' , blank=True)
    annoncement = models.ForeignKey(Announcement , on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        value = self.blog_title[0:250]
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)



