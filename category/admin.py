from django.contrib import admin

from category.models import Category

#to take the value automantically in the slug from the categor 
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')
    



    


# Register your models here.
admin.site.register(Category,CategoryAdmin)