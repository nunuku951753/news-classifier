from django.urls import path
from django.conf.urls import *
from . import views

# 定義網址及其對應的view
urlpatterns = [
    path('', views.news_list, name='news_list'), 
    url(r'^category/(?P<num>\d+)/$', views.news_nav, name='news_nav'), 
    path('news_add', views.news_add, name='news_add'),
    path('add_record', views.add_record, name='add_record'),
    path('base', views.base, name='base'),
]