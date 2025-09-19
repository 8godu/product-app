from django.urls import path
from . import views

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),  
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('', views.home, name='home'),

    # auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # products
    path('my/', views.my_products, name='my_products'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='edit_product'),
    path('products/<int:pk>/delete/', views.product_delete, name='delete_product'),

    # legacy optional routes (if your older templates link to these)
    path('product2/', views.product2, name='product2'),
    path('view/<int:pk>/', views.viewdetails, name='viewdetails'),
    path('update/<int:pk>/', views.update_legacy, name='update'),
    path('products/<int:pk>/contact/', views.contact_seller, name='contact_seller'),

]
