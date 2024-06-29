from django.db import models
from django_jalali.db import models as jmodel

class BaseModel(models.Model):
    created = jmodel.jDateTimeField(auto_now_add=True)
    updated = jmodel.jDateTimeField(auto_now=True)
    class Meta:
        abstract = True
