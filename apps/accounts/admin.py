from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	model = User
	list_display = ('email', 'role', 'status', 'is_staff', 'email_verified')
	list_filter = ('role', 'status', 'is_staff', 'email_verified')
	search_fields = ('email',)
	ordering = ('email',)
	
	# override fieldsets to remove 'username' and add our custom fields
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		('Personal info', {'fields': ('phone', 'phone_verified', 'email_verified')}),
		('Auth & Roles', {'fields': ('auth_provider', 'external_auth_id', 'role', 'status', 'notification_prefs')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'role', 'status'),
		}),
	)