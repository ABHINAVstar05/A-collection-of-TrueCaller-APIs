from django.contrib import admin
from .models.users import RegisteredUser, Contact
from .models.spam import Spam


class Admin_RegisteredUser(admin.ModelAdmin) :
    list_display = ['name', 'phone_number', 'email', 'last_login']
    #readonly_fields = ['name', 'phone_number', 'email', 'password']


class Admin_Contact(admin.ModelAdmin) :
    list_display = ['name', 'phone_number']
    #readonly_fields = ['name', 'phone_number', 'users']


class Admin_Spam(admin.ModelAdmin) :
    list_display = ['phone_number', 'spam_reported_count']
    #readonly_fields = ['phone_number', 'spam_reported_count']


admin.site.register(RegisteredUser, Admin_RegisteredUser)
admin.site.register(Contact, Admin_Contact)
admin.site.register(Spam, Admin_Spam)
