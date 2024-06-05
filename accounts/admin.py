from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OTP
from .forms import UserCreationForm, UserChangeForm


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']


admin.site.register(Session, SessionAdmin)


@admin.action(description="Mark selected users as verify")
def make_verify(modeladmin, request, queryset):
    queryset.update(is_verified=True)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin panel for user management with add and change forms plus password
    """
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ("id", "email", "phone_number", "username", "is_verified", "is_superuser", "is_active")
    list_filter = ("is_superuser", "is_active", "is_verified")
    searching_fields = ("email", "phone_number", "username")
    actions = ('make_verify', )
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("username", "email", "phone_number", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions", ),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    """
    """
    list_display = ("user_email", "user_phone_number", "code", "created_date")
    list_filter = ("created_date", )
    search_fields = ("user__email", "user__phone_number", "code")

    def user_phone_number(self, obj):
        return str(obj.user.phone_number) if obj.user.phone_number else '-'

    def user_email(self, obj):
        return str(obj.user.email)

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "referral_code", )
#     searching_fields = ("user", "referral_code", )


# class CredentialsAdmin(admin.ModelAdmin):
#     pass

