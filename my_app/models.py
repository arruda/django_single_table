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
#        dct = {self.type_field:self.type}
#        print dct
        return super(TypeAwareManager, self).get_query_set().filter(**{self.type_field:self.type})
  
class Foo(models.Model):
    "The single table model"

    TYPE_CHOICES = Choices(
                           (0,'foo','Foo'),
                           (1,'foo1','Foo1'),
                           (2,'foo2','Foo2'),
                           )

    type = models.SmallIntegerField(choices=TYPE_CHOICES,default=0)
    
    
    def get_fields(self):
    # make a list of field/values.
        dct={}
        for field in self.__class__._meta.fields:
            dct[field.attname] = field.value_to_string(self)
        return dct
    
    def __unicode__(self):
        return "%s - %s" %(self.pk,self.type)


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
    type = models.SmallIntegerField(choices=TYPE_CHOICES,default=0)
    foo = models.ForeignKey(Foo,related_name="%(class)s_list")
    bar = models.ForeignKey(Bar,related_name="%(class)s_list")
    
    
        
        
    def __unicode__(self):
        return "%s - %s - %s" %(self.pk, self.foo, self.bar)
    

for proxy_model in Foo.TYPE_CHOICES[1:]:
#    print proxy_model
    #:proxy_model
    exec(proxy_factory(proxy_model[1], 'Foo', 'type', proxy_model[0]))
    #:proxy_model_many_to_many_manager
    exec(manager_factory(proxy_model[1]+'Bar', proxy_model[1].lower(), proxy_model[0]))
    #:proxy_model_many_to_many
    exec(proxy_many_to_many_factory(proxy_model[1],'Bar', 'FooBar','foo__type', proxy_model[0]))
    many = vars().get(proxy_model[1]+'Bar')

    #: adds methods to access foo chields from bar.
    Bar = link_to_many_to_many_factory(Bar,'bar', many)
#    setattr(Bar,(proxy_model[1]+'Bar').lower(), link_to_many_to_may_factory(model_field, link_class, type_field, type))
    #add o many-to-many field no proxy model
#    setattr(Bar,proxy_model[1]+'Bar',models.ManyToManyField(vars()[proxy_model[1]],through=vars()[proxy_model[1]+'Bar']))
    


    
#class Foo1BarManager(models.Manager):
#        
#    def get_query_set(self):
#        return super(Foo1BarManager, self).get_query_set().filter(type=1)
#    
#    
#class Foo1Bar(FooBar):
#    
#    objects = Foo1BarManager()
#    class Meta:
#        proxy= True
#        
#    def save(self, *args, **kwargs):
#        self.type = 1
#        super(Foo1Bar, self).save(*args, **kwargs)
#
#setattr(Bar,'foo1s',models.ManyToManyField(Foo1,through=Foo1Bar))
#setattr(Bar,'foo1s',models.ManyToManyField(Foo1,through=Foo1Bar))
    