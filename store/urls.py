from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.MainView.as_view(), name="buy"),
    path('register/', views.sign_up, name="register"),
    path('login/', views.sign_in, name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('sell/', views.AddProduct.as_view(), name="sell"),
    # path('buy/<int:product_id>', views.product_view, name="product")
]
