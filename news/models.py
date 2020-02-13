from django.db import models
from django.contrib.auth.models import User #導入內建的使用者模組
from django.utils import timezone 
# Create your models here.

class NewsType(models.Model): # 新聞類型
    type_id = models.IntegerField()
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class News(models.Model): 
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 連接使用者模組，刪除時則會將關聯對象一併刪除
    title = models.CharField(max_length=200)
    content = models.TextField()
    keyword = models.CharField(max_length=100)
    category = models.IntegerField()
    
    created_date = models.DateTimeField(default=timezone.now) 
    created_time = models.DateTimeField(auto_now_add = True)
    
    def publish(self):
        self.created_date = timezone.now()
        self.save() 
        
    def __str__(self):
        return "<News: %s>" % self.title