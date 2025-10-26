from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.db.models import Q
import json

from .models import Category, Product, BlogPost


class HomeView(TemplateView):
    template_name = 'demo_app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_products'] = Product.objects.filter(is_active=True)[:6]
        context['recent_posts'] = BlogPost.objects.filter(is_published=True)[:3]
        context['categories'] = Category.objects.all()[:8]
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'demo_app/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category_id = self.request.GET.get('category')
        search = self.request.GET.get('search')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.select_related('category')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'demo_app/product_detail.html'
    context_object_name = 'product'


class CategoryListView(ListView):
    model = Category
    template_name = 'demo_app/category_list.html'
    context_object_name = 'categories'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'demo_app/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).select_related('author', 'category')


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'demo_app/blog_detail.html'
    context_object_name = 'post'


# API Views
def api_test(request):
    """Simple API test endpoint"""
    return JsonResponse({
        'message': 'Django Demo App API is working!',
        'status': 'success',
        'data': {
            'products_count': Product.objects.count(),
            'categories_count': Category.objects.count(),
            'blog_posts_count': BlogPost.objects.count(),
        }
    })


def api_health(request):
    """Health check endpoint"""
    try:
        # Test database connection
        Product.objects.count()
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'message': 'All systems operational'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }, status=503)


def api_products(request):
    """API endpoint to get all products"""
    products = Product.objects.filter(is_active=True).select_related('category')
    
    # Simple filtering
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    
    # Convert to JSON
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
            'category': product.category.name,
            'stock_quantity': product.stock_quantity,
            'is_active': product.is_active,
            'is_in_stock': product.is_in_stock,
            'created_at': product.created_at.isoformat(),
        })
    
    return JsonResponse({
        'products': products_data,
        'count': len(products_data)
    })


def api_categories(request):
    """API endpoint to get all categories"""
    categories = Category.objects.all()
    
    categories_data = []
    for category in categories:
        categories_data.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'products_count': category.products.count(),
            'created_at': category.created_at.isoformat(),
        })
    
    return JsonResponse({
        'categories': categories_data,
        'count': len(categories_data)
    })