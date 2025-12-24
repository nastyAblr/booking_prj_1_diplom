from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomUserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'created', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),
    )

@admin.register(CustomUserProfile)
class CustomUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tagline')
    search_fields = ['user__username', 'tagline']