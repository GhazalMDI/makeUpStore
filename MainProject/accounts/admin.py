from django.contrib import admin

from accounts.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number','first_name','last_name','is_active','is_admin')
    search_fields = ('is_admin',)
    list_filter = ('phone_number',)


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created','updated')
    search_fields = ('created',)
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('formatted_address',)

