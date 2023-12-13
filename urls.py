#from django.urls import path
from . import views
from django.urls import path, include
import test.views as test

urlpatterns = [
    path('', views.index, name='index'),
    #path('test/', include('test.urls')),
    path('personality_diagnosis/', include('personality_diagnosis.urls')),
    path('test/',test.index),
]