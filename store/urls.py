from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.store, name="buy"),
    path('register/', views.sign_up, name="register"),
    path('login/', views.sing_in, name="login"),
    # path('sell/', views.sell, name="sell"),
    # path('buy/<int:product_id>', views.product_view, name="product")
]
