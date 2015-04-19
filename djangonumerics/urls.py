"""url descriptions for django numerics."""
from django.conf.urls import patterns, url

from djangonumerics import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='django-numerics-index'),
    url(r'^help/(?P<code>.+)$', views.HelpView.as_view(),
        name='django-numerics-help'),
    url(r'^(?P<code>.+)$', views.EndpointView.as_view(),
        name='django-numerics-endpoint'),
)
