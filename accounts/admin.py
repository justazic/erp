from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from unfold.admin import ModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm as UnfoldUserChangeForm,
    UserCreationForm as UnfoldUserCreationForm,
    )

from .models import User


class CustomUserCreationForm(UnfoldUserCreationForm):
    class Meta(UnfoldUserCreationForm.Meta):
        model = User
        fields = ("username",
                  "email",
                  "first_name",
                  "last_name",
                  "role",
                  "avatar")


class CustomUserChangeForm(UnfoldUserChangeForm):
    class Meta(UnfoldUserChangeForm.Meta):
        model = User
        fields = "__all__"


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("first_name",
                    "last_name",
                    "username",
                    "email",
                    "role",
                    "is_expert",
                    "created_at",
                    "updated_at")
    search_fields = ("first_name",
                     "last_name",
                     "username",
                     "email")
    list_filter = ("role",
                   "is_expert",
                   "is_active",
                   "created_at")
    ordering = ("-id",)

    readonly_fields = ("created_at",
                       "updated_at",
                       "last_login",
                       "date_joined")

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
                        "phone",
                        "address"),
             }),
        ("Teacher info",
         {
             "fields": ("speciality",
                        "qualifications",
                        "is_expert"),
             }),
        ("Role",
         {
             "fields": ("role",),
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

    add_fieldsets = (
        (None,
         {
             "classes": ("wide",),
             "fields": (
                 "username",
                 "email",
                 "first_name",
                 "last_name",
                 "role",
                 "avatar",
                 "password1",
                 "password2",
                 "is_active",
                 "is_staff",
                 "is_superuser",
                 "groups",
                 "user_permissions",
                 ),
             }),
        )

    filter_horizontal = ("groups",
                         "user_permissions")