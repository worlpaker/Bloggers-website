from django.conf import settings
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Time")
    title = models.CharField(max_length=255, verbose_name="Title")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Time")
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    published_at = models.DateTimeField(null=True, blank=True, editable=True, default=timezone.now, verbose_name="Published Time")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category")
    title = models.CharField(max_length=200, verbose_name="Title")
    text = RichTextField(null=True, blank=True, verbose_name="Text")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title