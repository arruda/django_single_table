from django.db import models
from model_utils import Choices



class Foo(models.Model):
    "The single table model"
    TYPE_CHOICES = Choices(
                           (0,'foo','my_app.Foo'),
                           (1,'foo1','my_app.Foo1'),
                           (2,'foo2','my_app.Foo2'),
                           )
    
    type = models.SmallIntegerField(choices=TYPE_CHOICES,default=TYPE_CHOICES.foo)
    
    
    def __unicode__(self):
        return "%s - %s" %(self.pk,self.type)
    
class Foo1Manager(models.Manager):
        
    def get_query_set(self):
        return super(Foo1Manager, self).get_query_set().filter(type=1)
    
    
class Foo1(Foo):
    
    objects = Foo1Manager()
    class Meta:
        proxy= True
        
class Foo2Manager(models.Manager):
        
    def get_query_set(self):
        return super(Foo2Manager, self).get_query_set().filter(type=2)
    
    
class Foo2(Foo):
    
    objects = Foo2Manager()
    class Meta:
        proxy= True