from django.shortcuts import render
from django.shortcuts import redirect
from .models import News, NewsType
from .forms import PostForm
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt 
from .NewsClassifier import NewsClassifier
import os

me = get_user_model().objects.get(username="gina") 

# Create your views here.

def getTypeArr(cate_cnt, types):
    cate_dict = {}
    for cate in cate_cnt:
        cate_dict[cate['category']] = cate['cnt']
        
    type_arr = []
    for t in types:
        type_dict = {}
        type_dict['type_id'] = t.type_id
        type_dict['type_name'] = t.type_name
        if t.type_id in cate_dict.keys():
            type_dict['cnt'] = cate_dict[t.type_id]
        else:
            type_dict['cnt'] = 0
        type_arr.append(type_dict)
    return type_arr

# 定義templates路徑
def news_list(request):
    cate_cnt = News.objects.values('category').annotate(cnt=Count('category'))
    types = NewsType.objects.all()
    type_arr = getTypeArr(cate_cnt, types)   
    
    posts = News.objects.all().order_by('-created_date')
    return render(request, 'news/news_list.html', {'posts': posts, 'type_arr': type_arr})

def news_nav(request, num):
    cate_cnt = News.objects.values('category').annotate(cnt=Count('category'))
    types = NewsType.objects.all()
    type_arr = getTypeArr(cate_cnt, types)
    
    posts = News.objects.ﬁlter(category=num).order_by('-created_date')
    category = NewsType.objects.ﬁlter(type_id=num)
    return render(request, 'news/news_list.html', {'posts': posts, 'type_arr': type_arr, 'category': category[0]})

def news_add(request):
    cate_cnt = News.objects.values('category').annotate(cnt=Count('category'))
    types = NewsType.objects.all()
    type_arr = getTypeArr(cate_cnt, types)
    
    return render(request, 'news/news_add.html', {'post_form': PostForm, 'type_arr': type_arr})

@csrf_exempt
def add_record(request):  
    if request.POST:   
        title = request.POST['title']
        content = request.POST['content']
        
        root = os.getcwd()
        classifier = NewsClassifier('./news/model/7news_lstm_acc89.h5')
        words, ans = NewsClassifier.getPredictAns(classifier, content)
        word = str(words).replace('\'', '').replace('[', '').replace(']', '')
        
        News.objects.create(author=me, title=title, content=content, keyword=word, category=ans)
    return redirect('/news/category/'+str(ans))

def base(request):             
    return render(request, 'news/base.html', {})