from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    empid = models.CharField(max_length=8, unique=True)
    role = models.CharField(max_length=50)
    
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class TimeLog(models.Model):
    log_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def calculate_duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def _str_(self):
        return f"TimeLog for task {self.task.title} by {self.user.username}"


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def _str_(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"