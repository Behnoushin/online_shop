from django.db import models

class Template(models.Model):
    slug = models.SlugField(unique=True, max_length=100, verbose_name="شناسه یکتا")
    text = models.TextField(verbose_name="متن پیام")

    def __str__(self):
        return self.slug