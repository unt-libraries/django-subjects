from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('subjects/', include('subjects.urls')),

    path('accounts/login/', LoginView.as_view(
        template_name='subjects/login.html'), name="login"),

    path('accounts/logout/', LogoutView.as_view(
        template_name='subjects/logout.html'), name="logout"),
]
