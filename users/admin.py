from django.contrib import admin
from .models import User, PhoneOTP
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminChangeForm, UserAdminAddForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminAddForm

    list_display = ('phone', 'name', 'email', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('phone', 'email', 'password', 'image')}),
        ('Personal Info', {'fields': ('name', 'logged_in')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')})
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')})
    )

    search_fields = ('phone', 'email', 'name')
    ordering = ('last_login',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(PhoneOTP)