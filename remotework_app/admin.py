from django.contrib import admin
from .models import User
from .models import Task
from .models import TimeLog
from .models import Message

# Register your models here.

admin.site.register(User)
admin.site.register(Task)
admin.site.register(TimeLog)
admin.site.register(Message)