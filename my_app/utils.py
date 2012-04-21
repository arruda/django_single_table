# -*- coding: utf-8 -*-
"""
    my_app.utils
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c)  20/04/2012  by arruda.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
from django.db import models
import types


def replace_on_cast(attr):
    attr.replace_on_cast=True
    return attr

def hasmethod(obj, name):
    return hasattr(obj, name)

def cast(theclass):
  for x in filter(lambda x:"__" not in x and x not in dir(models.Model()), dir(theclass)):
     if hasmethod(theclass,x):
        print(x)
        
