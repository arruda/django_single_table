# -*- coding: utf-8 -*-
"""
    my_app.factory.manage_factory
    ~~~~~~~~~~~~~~

    Fabricates manager for proxy models

    :copyright: (c)  2012  by arruda.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from django.db import models




def factory(model, proxy):
    manager_name = model.__name__+"Manager"
    manager = type(manager_name,(models.Manager,))