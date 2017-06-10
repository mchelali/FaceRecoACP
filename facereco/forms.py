# -*- coding: utf-8 -*-
from django import forms
import os

class NewImage(forms.Form):
    image = forms.ImageField(label='Veulliez séléctioner une image')