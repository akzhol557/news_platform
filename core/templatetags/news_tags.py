from django import template
from core.models import Category, News
from django.db.models import Count

register = template.Library()


@register.simple_tag()
def show_categories():
    categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
    return categories


@register.simple_tag()
def show_categories_by_user(request):
    news = News.objects.filter(author=request.user)
    categories = Category.objects.all()
    lis_categories = []
    
    for category in categories:
        temp = [category.title, category.id, 0]
        for item in news:
            for cat1 in item.category.all():
                
                if category.id == cat1.id:
                    temp[2] += 1
        lis_categories.append(temp)
    

    return lis_categories