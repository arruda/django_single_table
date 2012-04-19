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
        
    objects = %(CLASS_NAME)sManager()
    class Meta:
        proxy= True
        
    def save(self, *args, **kwargs):
        self.%(TYPE_FIELD)s = %(TYPE)s
        super(%(CLASS_NAME)s, self).save(*args, **kwargs)
    
    
"""

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

