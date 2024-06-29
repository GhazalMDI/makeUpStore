from django.db import models

class Banner(models.Model):
    BANNERS_PART = (
        ('main','Main'),
        ('second','Second'),
        ('third', 'Third'),

    )
    image = models.ImageField(upload_to='home/%Y/%M/%d')
    part = models.CharField(max_length=20,choices=BANNERS_PART,default='main',null=True)
    category = models.ForeignKey('products.SecondCategory',models.SET_NULL,'banner_cat',null=True,blank=True)

    # def __str__(self):
    #     return self.part
