# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import QuerySet
from django.db.models.manager import Manager

# Create your models here.

class CustomManager(Manager):
    def all(self):
        return Manager.all(self).filter(isdelete=True)
#Student.objects.filter()

class NotDeletedManager(Manager):
    def all(self):
        return Manager.all(self).filter(isdelete=False)

class BatchDelManager(Manager):
   #重写get_queryset方法
    def get_queryset(self):
        return Manager.get_queryset(self).filter(isdelete=False)

    def filter(self, name=None, filter_func=None, **flags):
        #1.获取需要删除记录
        delList = Manager.get_queryset(self)
        #2.定义闭包方法执行修改isdelete=True操作
        def delete1(delqueryset):
            for dq in delqueryset:
                dq.isdelete = True
                dq.save()
        import types    #pytho
        #动态创建实例方法
        delList.delete = types.MethodType(delete1, delList)
        return delList

class Student(models.Model):
    sname = models.CharField(max_length=30)
    isdelete = models.BooleanField(default=False)

    objects = BatchDelManager()

    # objects = CustomManager()
    # show = NotDeletedManager()

    def __str__(self):
        return u'Student:%s %s' % (self.sname, self.isdelete)

    #Student.delete() 单个对象的删除,其它的是批量删除
    # def delete(self, using=None, keep_parents=False):
    #     self.isdelete = True
    #     self.save()
#Student.objects.all()  #默认返回全表数据


