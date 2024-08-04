from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


# email, name, nickname, phoneNumber, dateOfBirth
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ["created_at", "updated_at"]

    list_display = ('email', 'name', 'nickname', 'is_active')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password','name','phone_number')}),
        ('Personal info', {'fields': ('nickname',
                                      'membership_level',
                                      'created_at',
                                      'expiration_date',
                                      'last_login',
                                      'updated_at'
                                      )}),
        ('약관동의', {'fields': ('is_terms_agreement', 'is_info_use_agreement')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'nickname', 'phone_number',
                       'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'name', 'nickname')
    ordering = ('email', 'name', 'nickname')
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        return('created_at', 'updated_at')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)