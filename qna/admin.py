from django.contrib import admin

from django.contrib.auth.models import Group

from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Vote)

admin.site.unregister(Group)