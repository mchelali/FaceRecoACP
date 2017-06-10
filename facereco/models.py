# -*- coding: utf-8 -*-
from django.db import models
import os

class Image(models.Model):
    image = models.ImageField(upload_to='tmp/')

    def delete_(self, *args, **kwargs):
        os.remove(os.path.join('media/', self.image.name))
