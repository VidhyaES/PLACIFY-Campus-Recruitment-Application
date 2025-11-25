from django.contrib import admin

# Register your models here.
from .models import (Mock_test, Application, Resume, Post)

admin.site.register(Mock_test)
admin.site.register(Application)
admin.site.register(Resume)
admin.site.register(Post)