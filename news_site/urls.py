"""news_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from core.views import *

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', main_page, name='main_page'),
    path('category_view/<int:category_id>', category_view, name='category_view'),
    path('open_news/<int:news_id>/', open_page_news, name='open_page_news'),
    path('search/', search, name='search'),
    path('all_news/', all_news, name='all_news'),
    path('personal_area/', personal_area, name='personal_area'),
    path('personal_area/category/<int:category_id>', category_view_by_user, name='category_view_by_user'),
    path('personal_area/edit_news/<int:pk>', Edit_news.as_view(), name='edit_news'),
    path('personal_area/news_delete/<int:news_id>', news_delete, name='news_delete'),
    path('personal_area/open_news/<int:news_id>/', open_page_news_with_par, name='open_page_news_with_par'),
    path('login/', login_profile, name='login_profile'),
    path('search_with_prametrs/', search_with_prametrs, name='search_with_prametrs'),
    path('personal_area/create_news', create_news, name='create_news'),
    path('user_info/', user_info , name='user_info'),
    path('logout_profile/', logout_profile , name='logout_profile'),
    path('registration/', registration , name='registration'),
    path('about_site/', about_site , name='about_site'),
=======
    #path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
>>>>>>> 02f30cbbf266918bc2c1cab3f1a5a1f1b9e12b2b
]

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls, name='admin'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),

    path('', main, name='main'),

    path('news/', all_news, name='all_news'),
    path('news/<int:news_id>/', single_post, name='single_post'),
    path('news/<str:category_slug>/', news_filter_by_category, name='news_filter_by_category'),
    path('news/<int:news_id>/comment/', comments_create, name='create_comment'),

    path('galery/', all_gallies, name='all_gallies'),
    path('galery/<int:id>/', gallies_post, name='gallies_post'),
    path('galery/<str:category_slug>/', gellary_filter_by_category, name='gellary_filter_by_category'),

    path('simple_page/<str:slug>',simple_page, name='simple_post'),
    path('news_search/', search_news, name='search_news'),
    path('contacts/', TemplateView.as_view(template_name='contact.html'), name='contact'),

)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
