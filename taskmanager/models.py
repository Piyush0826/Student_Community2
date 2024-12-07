from django.db import models

class Task(models.Model):
    objects = None
    title = models.CharField(max_length=255)  # Task title
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for task creation

    def __str__(self):
        return self.title
