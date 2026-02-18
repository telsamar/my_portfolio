from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from accounts.views import home, catalog, contacts, reviews

urlpatterns = [
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('contacts/', contacts, name='contacts'),
    path('reviews/', reviews, name='reviews'),
]
