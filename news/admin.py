from django.contrib import admin
from .models import News, NewsType
# Register your models here.

# admin.site.register(News)

@admin.register(NewsType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'type_name')

@admin.register(News)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('author','title','content','keyword','category','created_date','created_time')