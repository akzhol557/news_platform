from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

def max_limit_size_upload(file):
    if file.size > 10485760:
        raise ValueError('Размер файла превышает ограниченного размера')
    else:
        return file

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(username, name, password, **other_fields)

    def create_user(self, username, name, password, **other_fields):

        user = self.model(username=username,
                          name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = 'Пользователи'

    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')
    name = models.CharField(max_length=150, blank=True, verbose_name='Имя и фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, verbose_name='Номер телефона')
    start_date = models.DateTimeField(default=timezone.now, verbose_name='Дата регистраций')
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False, verbose_name='Статус администратора')
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return f'{self.name} - {self.username}'


class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.title


class News(models.Model):
    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    image_1 = models.ImageField(upload_to='news_image/', validators=[max_limit_size_upload], verbose_name='Изображение')
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    information = models.TextField(verbose_name='Контент')
    category = models.ManyToManyField('Category', verbose_name='Категории')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    author = models.ForeignKey('NewUser', on_delete=models.PROTECT, verbose_name='Автор')
    view = models.IntegerField(default=0, null=True, verbose_name='Просмотры')

    def __str__(self):
        return f'{self.title} - {self.date}'

# Create your models here.
