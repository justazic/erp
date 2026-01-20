from django.contrib import admin
import unfold
from .models import User

class UserAdmin(unfold.admin.ModelAdmin):
  list_display = ('first_name', 'last_name', 'username', 'email', 'role', 'created_at', 'updated_at')
  search_fields = ('first_name', 'last_name', 'username', 'email')
  list_filter = ('role', 'is_active', 'created_at')
  ordering = ('-id',)
  readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
  fieldsets = (
    (None,
     {
       "fields": ("username",
                  "password"),
       }),
    ("Personal info",
     {
       "fields": ("first_name",
                  "last_name",
                  "email",
                  "avatar",
                  'role'),
       }),
    ("Permissions",
     {
       "fields": ("is_active",
                  "is_staff",
                  "is_superuser",
                  "groups",
                  "user_permissions"),
       }),
    ("Important dates",
     {
       "fields": ("last_login",
                  "date_joined",
                  "created_at",
                  "updated_at"),
       }),
    )




admin.site.register(User, UserAdmin)
