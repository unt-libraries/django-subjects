from django.conf.urls import include, url
from django.contrib import admin, auth

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^subjects/', include('subjects.urls')),
    url(r'^accounts/login/$', auth.views.login,
        {'template_name': 'subjects/login.html'}, name="login"),
    url(r'^accounts/logout/$', auth.views.logout,
        {'template_name': 'subjects/logout.html'}, name="logout"),
]
