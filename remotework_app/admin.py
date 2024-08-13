from django.contrib import admin
from .models import User
from .models import Task
from .models import TimeLog
from .models import Message

# Register your models here.
#This is a custom ModelAdmin class that defines how the User model should be displayed and edited in the admin interface.

class UserAdmin(admin.ModelAdmin):
    fields = ('username','email', 'first_name','last_name', 'role', 'date_joined','last_login', 'empid')

admin.site.register(User, UserAdmin)
admin.site.register(Task)
admin.site.register(TimeLog)
admin.site.register(Message)