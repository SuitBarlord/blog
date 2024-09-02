from django.contrib import admin

# Register your models here.
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('groups', 'user_permissions')}),
        (('Other'), {'fields': ('gender',)})
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {'fields': ('groups', 'user_permissions')}),
        (('Other'), {'fields': ('gender',)})
    )


admin.site.register(CustomUser, CustomUserAdmin)