from django.db import models

class AppAdmin(models.Model):
    admin_username = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin: {self.admin_username}, created on {self.created_at}"
