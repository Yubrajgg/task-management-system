from django.db import models
from django.contrib.auth import get_user_model

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='task_attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
