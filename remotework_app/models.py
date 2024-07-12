
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):
    id=models.AutoField(primary_key=True)
    empid=models.CharField(max_length=20,unique=True,db_index=True)
    email=models.EmailField(unique=True)
    full_name=models.CharField(max_length=100)
    role=models.CharField(max_length=50)
    join_date = models.DateField(null=True)
    password = models.CharField(max_length=128, default="some_password")
    confirm_password = models.CharField(max_length=128,default="some_password")
    def save(self, *args, **kwargs):
       # self.password = make_password(self.password)  # type: ignore
        super().save(*args, **kwargs)

    # Add related_name to avoid clash with auth.User.groups
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    # Add related_name to avoid clash with auth.User.user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    

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
        return f"TimeLog for task {self.task.task_name} by {self.user.username}"


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