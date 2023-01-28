from itertools import count
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
import datetime
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *


MAX_PAGE = 8 #Pagination. Max count news is in one page   


def regiter(string):
    string = string[0].upper() + string[1:len(string)]
    return string


def main_page(reqeust, reloading=False):
    if reloading is True:
        return redirect('/')
    news = News.objects.all().order_by('-date')
    three_last_news = News.objects.all().order_by('-date')[:3]
    pagin = Paginator(news, MAX_PAGE)
    page = reqeust.GET.get('page', None)
    if page is None:
        combine_pagin_news = pagin.get_page(1)
    else:
        combine_pagin_news = pagin.get_page(page)
    return render(reqeust, 'main.html', {'news': combine_pagin_news, 'corusels_news': three_last_news})


def all_news(reqeust):
    news = News.objects.all().order_by('-date')
    pagin = Paginator(news, MAX_PAGE)
    page = reqeust.GET.get('page', None)
    if page is None:
        combine_pagin_news = pagin.get_page(1)
    else:
        combine_pagin_news = pagin.get_page(page)
    three_last_news = News.objects.all().order_by('-date')[:3]
    return render(reqeust, 'all_news.html', {'news': combine_pagin_news, 'corusels_news': three_last_news})


def category_view(reqeust, category_id):
    news = News.objects.filter(category__id=category_id).order_by('-date')
    three_last_news = News.objects.order_by('-date')[:3]    
    pagin = Paginator(news, MAX_PAGE)
    page = reqeust.GET.get('page', None)
    if page is None:
        combine_pagin_news = pagin.get_page(1)
    else:
        combine_pagin_news = pagin.get_page(page)
    category = Category.objects.get(id=category_id)
    return render(reqeust, 'all_news.html', {'news': combine_pagin_news, 'corusels_news': three_last_news, 'category': category})


def news_delete(request, news_id):
    news = News.objects.get(id=news_id)
    if news.author.id == request.user.id:
        news.delete()
        messages.success(request, 'Публикация успешно удалено!')
    else:
        messages.warning(request, 'Вы не можете удалить работу другого сотрудника!')
    return redirect('/personal_area/')


def open_page_news(request, news_id):
    news = News.objects.get(id=news_id)
    two_last_news = News.objects.all().order_by('-date')[:2]
    if request.user.id != news.author.id:
        news.view += 1
        news.save()
    return render(request, 'open_news_of_the_id.html', {'news': news, 'two_last_news': two_last_news})


@login_required(login_url="/login")
def open_page_news_with_par(request, news_id):
    news = News.objects.get(id=news_id)
    two_last_news = News.objects.all().order_by('-date')[:2]
    return render(request, 'open_news_by_user.html', {'news': news, 'two_last_news': two_last_news})


def search(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        title = regiter(title)

        author_id = request.POST.get('author', None)
        if author_id is not None:
            news = News.objects.filter(author__id=author_id, title__icontains=title).order_by('-date')
            pagin = Paginator(news, MAX_PAGE)
            page = request.GET.get('page', None)
            if page is None:
                combine_pagin_news = pagin.get_page(1)
            else:
                combine_pagin_news = pagin.get_page(page)
            return render(request, 'personal_area.html', {'news': combine_pagin_news})
        
        news = News.objects.filter(title__icontains=title)
        three_last_news = News.objects.all().order_by('-date')[:3]
        pagin = Paginator(news, MAX_PAGE)
        page = request.GET.get('page', None)
        if page is None:
            combine_pagin_news = pagin.get_page(1)
        else:
            combine_pagin_news = pagin.get_page(page)
        return render(request, 'all_news.html', {'news': combine_pagin_news, 'corusels_news': three_last_news,})
    return redirect('/')


class Edit_news(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = News
    template_name = 'edit_news.html'
    form_class = CreateEditNewsForm
    success_url = '/personal_area/'
    success_message = 'Новости успешно отредотерованы!'
    login_url = "/login"

    
    def dispatch(self, request, *args, **kwargs):
        news_id = kwargs.get('pk')
        news = News.objects.get(id=news_id)
        if request.user != news.author:
            messages.error(request, 'Вы не можете редактировать чужую публикацию!')
            return redirect('/personal_area/')
        if request.method == 'POST':
            author_id = request.POST.get('author', None)
            if int(request.user.id) != int(author_id):
                messages.error(request, 'Вы не можете редактировать чужую публикацию!')
                return redirect('/personal_area/')
        return super().dispatch(request, *args, **kwargs)


    
def search_with_prametrs(request):
    if request.method == 'POST':
        date = request.POST.get('date', None)
        author = request.POST.getlist('author')
        category = request.POST.getlist('category')
        print(len(author), len(category), type(date))
        if date != '' and len(author) != 0 and len(category) == 0:
            news = News.objects.filter(date__date=date, author__in=request.POST.getlist('author')).distinct()
        elif len(author) != 0 and date == '' and len(category) == 0:
            news = News.objects.filter(author__in=request.POST.getlist('author')).distinct()
        elif date != '' and len(author) == 0 and len(category) == 0:
            news = News.objects.filter(date__date=date)
        elif date != '' and len(author) == 0 and len(category) != 0:
            news = News.objects.filter(date__date=date, category__in=request.POST.getlist('category')).distinct()
        elif len(author) == 0 and date == '' and len(category) != 0:
            news = News.objects.filter(category__in=request.POST.getlist('category')).distinct()
        elif len(author) != 0 and date == '' and len(category) != 0:
            news = News.objects.filter(category__in=request.POST.getlist('category'), author__in=request.POST.getlist('author')).distinct()
        else:
            news = News.objects.filter(date__date=date, category__in=request.POST.getlist('category'), author__in=request.POST.getlist('author')).distinct()
        three_last_news = News.objects.all().order_by('-date')[:3]
        pagin = Paginator(news, MAX_PAGE)
        page = request.GET.get('page', None)
        if page is None:
            combine_pagin_news = pagin.get_page(1)
        else:
            combine_pagin_news = pagin.get_page(page)
        return render(request, 'main.html', {'news': combine_pagin_news, 'corusels_news': three_last_news})
    form = SearchNewsForm()
    return render(request, 'search_with_prametrs.html', {'form': form})


@login_required(login_url="/login")
def personal_area(request):
    news = News.objects.filter(author__id=request.user.id).order_by('-date')
    pagin = Paginator(news, MAX_PAGE)
    page = request.GET.get('page', None)
    if page is None:
        combine_pagin_news = pagin.get_page(1)
    else:
        combine_pagin_news = pagin.get_page(page)
    return render(request, 'personal_area.html', {'news': combine_pagin_news})


@login_required(login_url="/login")
def category_view_by_user(request, category_id):
    news = News.objects.filter(author__id=request.user.id, category__id=category_id).order_by('date').reverse()

    pagin = Paginator(news, MAX_PAGE)
    page = request.GET.get('page', None)
    if page is None:
        combine_pagin_news = pagin.get_page(1)
    else:
        combine_pagin_news = pagin.get_page(page)
    category = Category.objects.get(id=category_id)
    return render(request, 'personal_area.html', {'news': combine_pagin_news, 'category': category})
    

def login_profile(request):
    if request.user.is_authenticated:
        return redirect(request.session['path'])
    if request.method == "POST":
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            path = request.POST.get('path', '/')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(path)
        messages.error(request, 'Не существует пользователя или неверный пароль')
        return render(request, "login.html", {"form_login": form_login})
    else:
        path = request.GET.get('next', '/')
        form_login = LoginForm()
    return render(request, "login.html", {"form_login": form_login, 'path': path})


@login_required(login_url="/login")
def create_news(request):
    if request.method == 'POST' and request.FILES:
        form = CreateEditNewsForm(request.POST)
        title = request.POST.get('title')
        information = request.POST.get('information')
        date = datetime.datetime.now()
        author = request.user

        fs = FileSystemStorage('media/news_image/')
        image_1 = request.FILES['image_1']
        fs.save(image_1.name, image_1)

    
        instance = News.objects.create(title=title, image_1=image_1, information=information,
                                date=date, author=author, view=0)

        categories = request.POST.getlist('category')
        for category in categories:
            temp = Category.objects.get(id=category)
            instance.category.add(temp)

        messages.success(request, 'Новости успешно опубликованы!')
        return redirect('/personal_area/')

    form = CreateEditNewsForm()
    return render(request, 'create_news.html', {'form': form})


@login_required(login_url="/login")
def user_info(request):
    if request.user.is_authenticated:
        return render(request, 'user_info.html', {})

@login_required(login_url="/login")
def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')

def registration(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.is_staff = True
                instance.is_admin = True
                instance.save()

                username = form.cleaned_data['username']
                password = form.cleaned_data['password2']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return personal_area(request)

                return redirect("/")
            else:
                messages.error(request, form.errors)
                return render(request, "register.html", {"form": form})
        else:
            form = RegisterForm()
        return render(request, "register.html", {"form": form})
    else:
        messages.error(request, 'Ты уже заригистрирован!')
        return main_page(request, reloading=True)

def about_site(request):
    return render(request, 'about_site.html', {})
# Create your views here.
