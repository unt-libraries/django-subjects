from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin, auth

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subjects/', include('subjects.urls')),
    path('accounts/login/', auth.views.login,
        {'template_name': 'subjects/login.html'}, name="login"),
    path('accounts/logout/url(', auth.views.logout,
        {'template_name': 'subjects/logout.html'}, name="logout"),
]
