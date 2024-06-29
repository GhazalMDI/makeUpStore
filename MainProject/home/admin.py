from django.contrib import admin

from home.models import *
@admin.register(Banner)
class Admin(admin.ModelAdmin):
    list_display = ('id','part','image')

