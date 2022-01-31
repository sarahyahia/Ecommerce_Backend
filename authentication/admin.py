from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
class MyUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    add_fieldsets = (
        (None, {'fields': ('email',"password","password2","isEmployer", 'first_name', 'last_name', )}),
    )
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'first_name', 'last_name','is_staff',)
                
            ),
        }),
    )


# admin.site.register(User, MyUserAdmin)