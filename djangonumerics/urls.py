"""url descriptions for django numerics."""
from django.conf.urls import patterns, url

from djangonumerics import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='django-numerics-index'),
)
