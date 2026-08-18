from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .models import Assessor


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "first_name", "last_name", "role", "is_staff"]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role",)}),)


admin.site.register(Assessor)