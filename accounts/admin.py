from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account,UserProfile
from django.utils.html import format_html

#make the change about the password in the admin pannel

class AccountAdmin(UserAdmin):
    list_display=('email','f_name','l_name','username','last_login','date_join','is_active')
    #to make them as like email link that when we clink we  go inside them
    list_display_links=('email','f_name','l_name')
    readonly_fields=('last_login','date_join')
    ordering=('-date_join',)

    filter_horizontal=()
    list_filter=()
    fieldsets=()        #it make the password as readonly 


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnails(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50px;" />'.format(object.profile_picture.url))
    
    thumbnails.short_description='Profile Picture'
    list_display=('thumbnails','user','city','state','country')

# Register your models here.
admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)