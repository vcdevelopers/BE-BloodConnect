from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.views.decorators.cache import never_cache

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^(?!static/)(?!api/)(?!django-admin/).*$', never_cache(TemplateView.as_view(template_name='index.html')), name='frontend'),
]

urlpatterns += staticfiles_urlpatterns()
