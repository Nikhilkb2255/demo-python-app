from django.urls import path
from . import views

app_name = 'demo_app'

urlpatterns = [
    # Web views
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('blog/', views.BlogPostListView.as_view(), name='blog_list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_detail'),
    
    # API endpoints
    path('api/test/', views.api_test, name='api_test'),
    path('api/health/', views.api_health, name='api_health'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/categories/', views.api_categories, name='api_categories'),
]
