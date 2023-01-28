
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.utils.safestring import mark_safe


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('username', 'name')
    ordering = ('-start_date',)
    list_display = ('username', 'name', 'phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'name', 'email', 'phone_number', 'is_superuser', 'password',)},
         ),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'name', 'email', 'phone_number', 'password1', 'password2', 'is_superuser',)}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)
admin.site.register(Category)


class NewsAdminForm(forms.ModelForm):
    information = forms.CharField(label='Контент', widget=CKEditorUploadingWidget())
    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(), queryset=Category.objects.all(), label='Категории')

    class Meta:
        model = News
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'author', 'view',)
    list_filter = ['date', 'author']
    search_fields = ('title__icontains',)
    readonly_fields = ('view', 'date', 'get_image')
    fields = ('title', 'image_1', 'information', 'category', 'author', 'view', 'date', 'get_image')
    form = NewsAdminForm

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image_1.url}" alt="" width="75%">')

    get_image.short_description = 'Изображение'

admin.site.site_header='Администрация и контроль данных'

# Register your models here.
