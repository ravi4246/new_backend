from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, HealthLog, TherapyPlan

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ('phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password'),
        }),
    )
    search_fields = ('phone',)
    ordering = ('phone',)

admin.site.register(User, MyUserAdmin)
admin.site.register(Profile)
admin.site.register(HealthLog)
admin.site.register(TherapyPlan)
