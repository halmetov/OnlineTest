"""Test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.views.static import serve
from Test import settings
from main.views import indexHandler, davayHandler, resultsHandler, insertHandler, analizeHandler, surveyHandler, \
    surveyItemHandler, surveyItemStartHandler

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }),
    path('davay', davayHandler),
    path('survey', surveyHandler),
    path('survey/<int:survey_item_id>/', surveyItemHandler),
    path('survey/<int:survey_item_id>/start/', surveyItemStartHandler),
    path('analize/<int:test_id>', analizeHandler),
    path('insert', insertHandler),
    path('results', resultsHandler),
    path('results/print', resultsHandler),
    path('', indexHandler),
]
