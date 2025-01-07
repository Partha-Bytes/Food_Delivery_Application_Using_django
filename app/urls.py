from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from app.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('home/', views.home, name='home'),
    path('add-dish/', views.add_dish, name='add_dish'),
    path('update_availability/<int:dish_id>/', views.update_availability, name='update_availability'),
    path('update_dish/<int:dish_id>/', views.update_dish, name='update_dish'),
    path('delete-dish/<int:id>/', views.delete_dish, name='delete_dish'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('view-menu/', views.view_menu, name='view_menu'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:dish_id>/', views.remove_cart_item, name='remove_from_cart'),
    path('profile/', views.profile, name='profile'),
    path('reviews/', views.reviews, name='reviews'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
