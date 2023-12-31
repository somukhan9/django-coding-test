from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=False, null=False)
    due_date = models.DateTimeField()
    create_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    priority = models.CharField(max_length=10, choices=(
        ('low', 'Low'), ('medium', 'Medium'), ('high', 'High')))
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"This image belongs to {self.task.title}"
