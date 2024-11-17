from django.contrib import admin
from .models import Book

class Bookadmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year') 
    search_fields = ('title', 'author') 
    list_filter = ('publication_year')


admin.site.register(Book)


from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
