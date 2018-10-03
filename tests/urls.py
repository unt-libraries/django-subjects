from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^subjects/', include('subjects.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'subjects/login.html'}, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'subjects/logout.html'}, name="logout"),
]
