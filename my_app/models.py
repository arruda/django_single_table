from django.db import models
from model_utils import Choices
from factory import manager_factory, proxy_factory



class Foo(models.Model):
    "The single table model"
    TYPE_CHOICES = Choices(
                           (0,'foo','Foo'),
                           (1,'foo1','Foo1'),
                           (2,'foo2','Foo2'),
                           )
    
    type = models.SmallIntegerField(choices=TYPE_CHOICES,default=TYPE_CHOICES.foo)
    
    
    def __unicode__(self):
        return "%s - %s" %(self.pk,self.type)

for proxy_model in Foo.TYPE_CHOICES:
    exec(manager_factory(proxy_model[1], 'type', proxy_model[0]))
    exec(proxy_factory(proxy_model[1], 'Foo', 'type', proxy_model[0]))

#exec(manager_factory('Foo1', 'type', 1))
#exec(proxy_factory('Foo1', 'Foo', 'type', 1))

#class Foo1(Foo):
#    
#    objects = Foo1Manager()
#    class Meta:
#        proxy= True
#        
#    def save(self, *args, **kwargs):
#        self.type = 1
#        super(Foo1, self).save(*args, **kwargs)
            
#class Foo2Manager(models.Manager):
#        
#    def get_query_set(self):
#        return super(Foo2Manager, self).get_query_set().filter(type=2)
#    
#    
#class Foo2(Foo):
#    
#    objects = Foo2Manager()
#    class Meta:
#        proxy= True
        
        
class Bar(models.Model):
    "a class that has connection to other proxies"
    
#    foo1 = models.ForeignKey(Foo1)#,related_name="bars")
#    foo2 = models.ForeignKey(Foo2)#,related_name="bars")
#    foos = models.ManyToManyField(Foo)#,through=FooBar)
    
    def __unicode__(self):
        return "%s" %(self.pk)
    
    
class FooBar(models.Model):
    "many to many foo to bars"
    TYPE_CHOICES = Choices(
                           (0,'foo','Foo'),
                           (1,'foo1','Foo1'),
                           (2,'foo2','Foo2'),
                           )
    foo = models.ForeignKey(Foo)
    bar = models.ForeignKey(Bar)
    type = models.SmallIntegerField(choices=TYPE_CHOICES,default=TYPE_CHOICES.foo)
    
    def __unicode__(self):
        return "%s - %s - %s" %(self.pk, self.foo, self.bar)
    
    
class Foo1BarManager(models.Manager):
        
    def get_query_set(self):
        return super(Foo1BarManager, self).get_query_set().filter(type=1)
    
    
class Foo1Bar(FooBar):
    
    objects = Foo1BarManager()
    class Meta:
        proxy= True
        
    def save(self, *args, **kwargs):
        self.type = 1
        super(Foo1Bar, self).save(*args, **kwargs)

setattr(Bar,'foo1s',models.ManyToManyField(Foo1,through=Foo1Bar))
#setattr(Bar,'foo1s',models.ManyToManyField(Foo1,through=Foo1Bar))
    