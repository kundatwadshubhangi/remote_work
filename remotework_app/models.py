from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    #id=models.IntegerField(primary_key=True)
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

#add related_name to avoid clash with auth.Usert.groups
    groups=models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='the groups this user belongs to a user will get all permission granted to each of there groups.',
        verbose_name='groups',
    )

#add related_name to avoid clash with auth.User.user_permission
    user_permissions=models.ManyToManyField(
        'auth.permission',
        related_name='custom_user_set',
        blank=True,
        help_text='specific permission for this user',
        verbose_name='user permission',
    )
    def _str_(self):
        return self.username
    

class Task(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(max_length=50)
    priority=models.CharField(max_length=50)
    due_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title