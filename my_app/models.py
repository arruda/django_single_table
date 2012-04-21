from django.db import models
from model_utils import Choices
from factory import manager_factory, proxy_factory, proxy_many_to_many_factory, link_to_many_to_many_factory
from utils import replace_on_cast

class TypeAwareManager(models.Manager):
    
    def __init__(self,type_field, type, *args, **kwargs):
        super(TypeAwareManager, self).__init__(*args, **kwargs)
        self.type = type
        self.type_field = type_field
    
    def get_query_set(self):
        return super(TypeAwareManager, self).get_query_set().filter(**{self.type_field:self.type})
  
class Foo(models.Model):
    "The single table model"

    TYPE_CHOICES = Choices(
                           (0,'foo','Foo'),
                           (1,'foo1','Foo1'),
                           )

    type = models.SmallIntegerField(choices=TYPE_CHOICES,default=0)
    
    
    def __unicode__(self):
        return "%s - %s" %(self.pk,self.type)


class Foo1(Foo):
        
    objects = TypeAwareManager('type',1)
    
    def __cast_from(self,super_instance):
        #change this instance fields for the super_instance one
        #but only the ones that matter.
        
        pass

    
    def __init__(self, *args, **kwargs):        
        super(Foo1, self).__init__(*args, **kwargs)
        #:cast
        if args != ():
            if isinstance(args[0],Foo):
                self.__cast_from(args[0])
        self.type = 1

    class Meta:
        proxy= True
    
    def save(self, *args, **kwargs):
        self.type = 1
        super(Foo1, self).save(*args, **kwargs)
        
        

    
class FooBar(models.Model):
    "many to many foo to bars"
    
    foo = models.ForeignKey('my_app.Foo',related_name="%(class)s_list")
    bar = models.ForeignKey('my_app.Bar',related_name="%(class)s_list")
    
    value = models.SmallIntegerField("Value",default=0)
        
        
    def __unicode__(self):
        return "%s - %s - %s" %(self.pk, self.foo, self.bar)
    


class Foo1Bar(FooBar):
    
    objects = TypeAwareManager('foo_type',1)
    
    class Meta:
        proxy= True
    
class Bar(models.Model):
    "a class that has connection to other proxies"
    foos = models.ManyToManyField('my_app.Foo1',related_name='bars_list',through='my_app.Foo1Bar')
    
    def __unicode__(self):
        return "%s" %(self.pk)
    
    
    

    