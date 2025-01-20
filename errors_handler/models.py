from django.db import models

class ExceptionLog(models.Model):
    title = models.CharField(max_length=255)
    trace = models.TextField()  
    url = models.URLField() 
    request_body = models.TextField(null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
