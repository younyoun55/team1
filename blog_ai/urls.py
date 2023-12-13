
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("input/", include("personality_diagnosis.urls")),
#    path('admin/', admin.site.urls),
]
