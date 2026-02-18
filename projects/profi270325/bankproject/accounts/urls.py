from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView, home, catalog, contacts, reviews, order_item
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/order/<int:item_id>/', order_item, name='order_item'),
    path('contacts/', contacts, name='contacts'),
    path('reviews/', reviews, name='reviews'),
]
