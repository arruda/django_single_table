"""
    my_app.factory
    ~~~~~~~~~~~~~~

    Fabricates manager for proxy models
    and the proxy models

    :copyright: (c)  2012  by arruda.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

MANAGER_TEMPLATE = \
"""
class %(CLASS_NAME)sManager(models.Manager):
        
    def get_query_set(self):
        return super(%(CLASS_NAME)sManager, self).get_query_set().filter(%(TYPE_FIELD)s=%(TYPE)s)
    
    
"""

PROXY_TEMPLATE = \
"""
class %(CLASS_NAME)s(%(SUPER_CLASS)s):
        
    objects = TypeAwareManager('%(TYPE_FIELD)s',%(TYPE)s)
    
    def __cast_from(self,super_instance):
        for k,v in instance.get_fields().items():
            if k in self.get_fields():
                self.__setattr__(k,v)

    
    def __init__(self, *args, **kwargs):        
        super(%(CLASS_NAME)s, self).__init__(*args, **kwargs)
        #:cast
        if args != ():
            if isinstance(args[0],%(SUPER_CLASS)s):
                self.__cast_from(args[0])
        self.%(TYPE_FIELD)s = %(TYPE)s

    class Meta:
        proxy= True
    
    def save(self, *args, **kwargs):
        self.%(TYPE_FIELD)s = %(TYPE)s
        super(%(CLASS_NAME)s, self).save(*args, **kwargs)
"""
    

MANY_TO_MANY_TEMPLATE =\
"""
class %(CLASS_A_NAME)s%(CLASS_B_NAME)s (%(SUPER_CLASS)s):
    
    objects = TypeAwareManager('%(TYPE_FIELD)s',%(TYPE)s)
    
    class Meta:
        proxy= True
        
"""

def link_to_many_to_many_factory(cls,model_field,link_class):
    def link(self):
        print link_class.__name__
        return link_class.objects.filter(**{model_field : self})

    setattr(cls,link_class.__name__.lower()+"_list", link)
    return cls
    
def manager_factory(class_name,type_field_name,type):
    format_dict = {
                   'CLASS_NAME':class_name,
                   'TYPE_FIELD':type_field_name,
                   'TYPE':type,
                   }
    return MANAGER_TEMPLATE % format_dict


def proxy_factory(class_name,super_class,type_field_name,type):
    format_dict = {
                   'CLASS_NAME':class_name,
                   'SUPER_CLASS':super_class,
                   'TYPE_FIELD':type_field_name,
                   'TYPE':type,
                   }
    
    return PROXY_TEMPLATE % format_dict


def proxy_many_to_many_factory(class_a_name,class_b_name,super_class,type_field_name,type):
    format_dict = {
                   'CLASS_A_NAME':class_a_name,
                   'CLASS_B_NAME':class_b_name,
                   'SUPER_CLASS':super_class,
                   'TYPE_FIELD':type_field_name,
                   'TYPE':type,
                   }
#    print  MANY_TO_MANY_TEMPLATE % format_dict
    return MANY_TO_MANY_TEMPLATE % format_dict
